# @Author: Antero Maripuu Github:<machinelearningxl>
# @Date : 2019-07-31 17:38
# @Email:  antero.maripuu@gmail.com
# @Project: Coursera
# @Filename : Week_2.py

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
census_df = pd.read_csv('census.csv')
census_df.head()

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head(15)


def answer_zero():
    # Question 0 (Example)
    # What is the first country in df?
    # This function should return a Series.
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

def answer_two():
    # Question 1
    # Which country has won the most gold medals in summer games?
    # This function should return a single string value.
    return df["Gold"].idxmax()

def answer_three():
    # Question 3
    # Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative
    # to their total gold medal count?
    # Only include countries that have won at least 1 gold in both summer and winter. This function should return a
    # single string value.

    only_gold = df[(df["Gold"]>0)&(df["Gold.1"]>0)]
    only_gold = (((only_gold['Gold'] - only_gold['Gold.1'])).abs()/only_gold['Gold.2'])
    return only_gold.idxmax()

def answer_four():
    # Question 4
    # Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2)
    # counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. The function
    # should return only the column (a Series object) which you created, with the country names as indices.
    # This function should return a Series named Points of length 146
    points = df["Gold.2"] * 3 + df["Silver.2"] * 2 + df["Bronze.2"] * 1
    return points

def answer_five():
    # Question 5
    # Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
    # This function should return a single string value.

    return census_df[census_df['SUMLEV']==50].groupby("STNAME")["CTYNAME"].count().idxmax()

def answer_six():
    # Only looking at the three most populous counties for each state, what are the three most populous
    # states (in order of highest population to lowest population)? Use CENSUS2010POP.
    # This function should return a list of string values.

    census_df = pd.read_csv ('census.csv')
    census_df = census_df[census_df['SUMLEV'] == 50]
    census_df = census_df.groupby ('STNAME')['CENSUS2010POP'].apply (lambda x: x.nlargest (3).sum ())
    return list(census_df.nlargest(3).index.values)


def answer_seven():

    # Which county has had the largest absolute change in population within the period 2010-2015?
    # Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
    # e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest
    # change in the period would be |130-80| = 50. This function should return a single string value.
    census_df = pd.read_csv ('census.csv')
    census_df = census_df[census_df['SUMLEV'] == 50]
    columns_to_keep = ['STNAME',
                       'CTYNAME',
                       'POPESTIMATE2010',
                       'POPESTIMATE2011',
                       'POPESTIMATE2012',
                       'POPESTIMATE2013',
                       'POPESTIMATE2014',
                       'POPESTIMATE2015']
    census_df = census_df[columns_to_keep]
    census_df = census_df.set_index ("CTYNAME")
    census_df["Diff"] = (census_df.max(axis=1) - census_df.min(axis=1)).abs()
    census_df = census_df["Diff"].idxmax()
    return census_df

def answer_eight():
    # Question 8
    # In this datafile, the United States is broken up into four regions using the "REGION" column.
    # Create a query that finds the counties that belong to regions 1 or 2, whose name starts with
    # 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
    # This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same
    # index ID as the census_df (sorted ascending by index).
    def answer_eight():
        census_df = pd.read_csv ('census.csv')
        census_df = census_df[(census_df['SUMLEV'] == 50) & ((census_df['REGION'] == 1) | (census_df['REGION'] == 2))]
        columns_to_keep = ['STNAME',
                           'CTYNAME',
                           "REGION",
                           'POPESTIMATE2014',
                           'POPESTIMATE2015']
        census_df = census_df[columns_to_keep]
        census_df = census_df[census_df["CTYNAME"].apply (lambda x: x.startswith ("Washington"))]
        census_df = census_df[census_df['POPESTIMATE2014'] < census_df['POPESTIMATE2015']]
    return census_df[["STNAME", "CTYNAME"]]

