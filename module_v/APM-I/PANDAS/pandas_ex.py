import pandas as pd
import sqlite3
import re

con = sqlite3.connect("IMDB-Movie-Data.sqlite")
df = pd.read_sql_query("SELECT * FROM films", con)

# print(df.info())

# E0
# boolean = df['Actors'].str.contains('Michael Fassbender')
# print(df[boolean].sort_values('Rating', ascending=False).iloc[0])


# E1
# print(df[(df['Director'] == 'J.J. Abrams') & (df['Year'] == '2013')])


# E2
# kboolean = df['Actors'].str.contains('Keanu Reeves')
# wboolean = df['Actors'].str.contains('Willem Dafoe')
# gboolean = df['Genre'].str.contains('Action')
#
# print(df[(kboolean) & (wboolean) & (gboolean)])


# E3
# qboolean = df['Director'].str.contains('Quentin Tarantino')
#
# print(df[qboolean].describe())


# E4
# tarantino = df[df['Director'].str.contains('Tarantino')]
# print(tarantino)
# # a=tarantino[['Revenue (Millions)', 'Rating']].corr()
# # a=tarantino['Revenue (Millions)'].corr(tarantino['Rating'])
# print(a)


# E5
# def query_title(title):
#     return pd.read_sql_query(f"SELECT * FROM films WHERE Title == {title}", con)
#
#
# print(query_title('"Guardians of the Galaxy"'))


def insert_record(record):
    # if len(record) != len():
    #     print('Error ya sabes qué')
    #     exit(1)
    values = ''
    for field in record:
        values+=str(field)+','
    values = values[:-1]
    print(values)
    pd.read_sql_query(f"INSERT INTO films ('Rank', 'Title', 'Genre', 'Description', 'Director', 'Actors', 'Year', 'Runtime (Minutes)', 'Rating', 'Votes', 'Revenue (Millions)', 'Metascore') VALUES({values})", con)

insert_record([1,2,3,4,5,6,7,8,9,10,11,12])