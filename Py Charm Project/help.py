import numpy as np

def fetch_medal_tally(df, years, nation):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if years == 'Overall' and nation == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and nation != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == nation]
    if years != 'Overall' and nation == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and nation != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == years) & (medal_df['region'] == nation)]

    if flag == 1:
        z = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        z = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    z['total'] = z['Gold'] + z['Silver'] + z['Bronze']

    z['Gold'] = z['Gold'].astype('int')
    z['Silver'] = z['Silver'].astype('int')
    z['Bronze'] = z['Bronze'].astype('int')
    z['total'] = z['total'].astype('int')


    return z

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total']= medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def nation_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.reverse()
    years.insert(0,'Overall')


    nation = np.unique(df['region'].dropna().values).tolist()
    nation.sort()
    nation.insert(0, 'Overall')

    return years, nation

def nations_participated_over_time(df):
    country_breakthrough = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    country_breakthrough = country_breakthrough.rename(
        columns={'Year': 'Total Years', 'count': 'Number of Nations participated'})

    return country_breakthrough

def events_hosted_over_time(df):
    events_over_time = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')
    events_over_time = events_over_time.rename(columns= {'Year' : 'Years', 'count' : 'Number of Events hosted'})

    return events_over_time

def athletes(df):
    athletes_participated = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    athletes_participated = athletes_participated.rename(columns={'Year': 'Years', 'count': 'Total Athletes'})

    return athletes_participated


def successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    q = temp_df['Name'].value_counts().reset_index().head(15).merge(df)[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    q.rename(columns={'count': 'Medals'}, inplace=True)
    return q

def medal_statistics_over_years(df, country):

    temporary_df = df.dropna(subset=['Medal'])
    temporary_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temporary_df[temporary_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def nation_sports_heatmap(df, country):
    temporary_df = df.dropna(subset=['Medal'])
    temporary_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temporary_df[temporary_df['region'] == country]

    pivot_table = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pivot_table


def successful_nation_wise(df, nation):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == nation]

    q = temp_df['Name'].value_counts().reset_index().head(20).merge(df)[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    q.rename(columns={'count': 'Medals'}, inplace=True)
    return q

def wt_vs_ht(df,sport):
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    ath_df['Medal'].fillna('No Medal', inplace=True)
    if sport!= 'Overall':
        tdf = ath_df[ath_df['Sport'] == sport]
        return tdf
    else:
        return ath_df

def m_vs_w(df):
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    men = ath_df[ath_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = ath_df[ath_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final





