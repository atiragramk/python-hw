import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/02_Filtering_%26_Sorting/Euro12/Euro_2012_stats_TEAM.csv')


my_columns = ['Team', 'Yellow Cards', 'Red Cards']

cards_stat = df[my_columns]

team_count = df.count().Team

top_scoring_team = df[df.Goals > 6]
