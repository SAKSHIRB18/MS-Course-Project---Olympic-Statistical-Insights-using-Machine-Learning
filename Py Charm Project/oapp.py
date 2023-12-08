import streamlit as st
import pandas as pd
import prep, help
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = prep.preprocess(df, region_df)

st.sidebar.title("Olympics Statistical Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Scoreboard','In-Depth Analysis','National Analysis','Athlete Evaluation')
)

#st.dataframe(df)

if user_menu == 'Medal Scoreboard':
    st.sidebar.header("Medal Scoreboard")
    years, nation = help.nation_year_list(df)
    selected_year = st.sidebar.selectbox("Which Year",years)
    selected_nation = st.sidebar.selectbox("Choose Nation", nation)

    medal_tally = help.fetch_medal_tally(df,selected_year, selected_nation)
    if selected_year == 'Overall' and selected_nation == 'Overall' :
        st.title("Overall Statistics")
    if selected_year != 'Overall' and selected_nation == 'Overall':
        st.title("Statistical Distribution of Olympics Medal " + str(selected_year) )
    if selected_year == 'Overall' and selected_nation != 'Overall':
        st.title("In All Performance of " + selected_nation  )
    if selected_year != 'Overall' and selected_nation != 'Overall':
        st.title(selected_nation + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == "In-Depth Analysis":
    editions = df['Year'].unique().shape[0] - 1
    total_cities = df['City'].unique().shape[0]
    no_of_sports = df['Sport'].unique().shape[0]
    no_of_events = df['Event'].unique().shape[0]
    total_athletes = df['Name'].unique().shape[0]
    participating_nations = df['region'].unique().shape[0]

    st.title("Statistics Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Years")
        st.title(editions)
    with col2:
        st.header("Hosting Cities")
        st.title(total_cities)
    with col3:
        st.header('Total Sports')
        st.title(no_of_sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events Organised")
        st.title(no_of_events)
    with col2:
        st.header("Athletes Participated")
        st.title(total_athletes)
    with col3:
        st.header("Nations Participated")
        st.title(participating_nations)

    country_breakthrough = help.nations_participated_over_time(df)
    fig = px.line(country_breakthrough, x= 'Total Years', y= 'Number of Nations participated')
    st.title("Total Number of Nations participated over Years")
    st.plotly_chart(fig)

    events_over_time = help.events_hosted_over_time(df)
    fig2 = px.pie(events_over_time, names='Years', values='Number of Events hosted', title='Number of Events hosted in Olympics over time.')
    st.title("Total Events hosted over Years")
    st.plotly_chart(fig2)

    athletes_participated = help.athletes(df)
    fig3 = px.line(athletes_participated, x= 'Years', y= 'Total Athletes')
    st.title(" Athletes Participated in Olympics over Years")
    st.plotly_chart(fig3)

    st.title("Each Sport held over years")
    fig, ax = plt.subplots(figsize=(18,18))
    w = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(w.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Outstanding Athletes")
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Choose a Sport", sports_list)
    q = help.successful(df, selected_sport)
    st.table(q)

if user_menu == 'National Analysis':

    st.sidebar.title('Olympic Analysis according to each Nation')

    nation_list = df['region'].unique().tolist()
    nation_list.sort(key=lambda x: str(x))

    selected_nation = st.sidebar.selectbox('Choose a Country', nation_list)

    country_df = help.medal_statistics_over_years(df, selected_nation)
    fig5 = px.pie(country_df, names='Year', values='Medal')
    st.title("Medal statistics for " + selected_nation + " over the years")
    st.plotly_chart(fig5)

    st.title("Performance of " + selected_nation + " in the following Sports")
    pivot_table = help.nation_sports_heatmap(df, selected_nation)
    fig, ax = plt.subplots(figsize=(18, 18))
    ax = sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)

    st.title("Top 20 Athletes of " + selected_nation)
    top20_df = help.successful_nation_wise(df,selected_nation)
    st.table(top20_df)

if user_menu == 'Athlete Evaluation':
    ath_df = df.drop_duplicates(subset=['Name', 'region'])

    z1 = ath_df['Age'].dropna()
    z2 = ath_df[ath_df['Medal'] == 'Gold']['Age'].dropna()
    z3 = ath_df[ath_df['Medal'] == 'Silver']['Age'].dropna()
    z4 = ath_df[ath_df['Medal'] == 'Bronze']['Age'].dropna()

    fig6 = ff.create_distplot([z1, z2, z3, z4],
                              ['Total Age', 'Gold Medal Winners', 'Silver Medal Winners', 'Bronze Medal Winners'],
                              show_hist=False, show_rug=False)
    fig6.update_layout(autosize=False, width=700, height=600)
    st.title("Age Analysis")
    st.plotly_chart(fig6)

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    st.title("Medal Analysis with respect to Height, Weight and Gender")
    selected_sport = st.selectbox("Choose a Sport", sports_list)
    tdf = help.wt_vs_ht(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style=tdf['Sex'], s=80, data=tdf)

    st.pyplot(fig)

    st.title("Medal Analysis wrt Gender")
    final = help.m_vs_w(df)
    fig8 = px.line(final, x='Year', y=["Male", "Female"])
    fig8.update_layout(autosize=False, width=700, height=600)
    st.plotly_chart(fig8)

















