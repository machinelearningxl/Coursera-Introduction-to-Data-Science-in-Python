# @Author: Antero Maripuu Github:<machinelearningxl>
# @Date : 2019-08-03 20:26
# @Email:  antero.maripuu@gmail.com
# @Project: Coursera
# @Filename : Week_3.py

#Assignment 3 - More Pandas

#This assignment requires more individual learning then the last one did - you are encouraged to check out the pandas
# documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag
# them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and
# the course staff.

#Question 1 (20%)

#Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable
# electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable
# name of energy.

#Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer
# and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and
# you should change the column labels so that the columns are:

#['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

#Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing
# data (e.g. data with "...") make sure this is reflected as np.NaN values.

#Rename the following list of countries (for use in later questions):
#"Republic of Korea": "South Korea",
#"United States of America": "United States",
#"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
#"China, Hong Kong Special Administrative Region": "Hong Kong"

#There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g.
#'Bolivia (Plurinational State of)' should be 'Bolivia',
#'Switzerland17' should be 'Switzerland'.

#Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015
# from World Bank. Call this DataFrame GDP.

#Make sure to skip the header, and rename the following list of countries:

#"Korea, Rep.": "South Korea",
#"Iran, Islamic Rep.": "Iran",
#"Hong Kong SAR, China": "Hong Kong"


#Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file
# scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this
# DataFrame ScimEn.

#Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names).
# Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

#The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable
# documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
# '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

#This function should return a DataFrame with 20 columns and 15 entries.

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import time

pd.set_option('display.max_rows', 500)

data = pd.read_excel("Energy Indicators.xls", sheet_name=0, skiprows=17, skipfooter=38, na_values="...").iloc[:, 2:6]
data_1 = pd.read_csv("world_bank.csv", skiprows=4)
data_2 = pd.read_excel("scimagojr.xlsx")

def answer_one():
    energy = pd.DataFrame(data).rename(columns ={"Unnamed: 2":"Country", "Petajoules":"Energy Supply",
                                             "Gigajoules":"Energy Supply per Capita",
                                             "%":"% Renewable"})
    energy['Country'] = energy['Country'].str.replace('\d+', '').replace({"Korea, Rep.": "South Korea",
                                                                        "Iran, Islamic Rep.": "Iran",
                                                                        "Hong Kong SAR, China": "Hong Kong",
                                                                        "Republic of Korea": "South Korea",
                                                                        "United States of America": "United States",
                                                                        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                                        "China, Hong Kong Special Administrative Region": "Hong Kong"}).str.replace(r" \(.*\)","")
    energy["Energy Supply"] =energy["Energy Supply"].apply(lambda x: x*1000000)



    gdp = pd.DataFrame(data_1, columns=["Country Name","2006",
                                    "2007","2008","2009",
                                    "2010","2011","2012",
                                    "2013","2014","2015"]).rename(columns = {"Country Name":"Country"})
    gdp['Country'] = gdp['Country'].replace({"Korea, Rep.": "South Korea",
                                         "Iran, Islamic Rep.": "Iran",
                                         "Hong Kong SAR, China": "Hong Kong"})

    ScimEn = pd.DataFrame(data_2)

    df = pd.merge(ScimEn, energy, how='inner',left_on='Country', right_on='Country')
    df =pd.merge(df, gdp, how='inner',left_on='Country', right_on='Country').set_index("Country").iloc[0:15]
    return df

#print(answer_one())


def answer_two():
    # Question 2 (6.6%)

    # The previous question joined three datasets then reduced this to just the top 15 entries.
    # When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
    # This function should return a single number.

    energy = pd.DataFrame (data).rename (columns={"Unnamed: 2": "Country", "Petajoules": "Energy Supply",
                                                  "Gigajoules": "Energy Supply per Capita",
                                                  "%": "% Renewable"})
    energy['Country'] = energy['Country'].str.replace ('\d+', '').replace ({"Korea, Rep.": "South Korea",
                                                                            "Iran, Islamic Rep.": "Iran",
                                                                            "Hong Kong SAR, China": "Hong Kong",
                                                                            "Republic of Korea": "South Korea",
                                                                            "United States of America": "United States",
                                                                            "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                                            "China, Hong Kong Special Administrative Region": "Hong Kong"}).str.replace (
        r" \(.*\)", "")
    energy["Energy Supply"] = energy["Energy Supply"].apply (lambda x: x * 1000000)

    gdp = pd.DataFrame (data_1, columns=["Country Name", "2006",
                                         "2007", "2008", "2009",
                                         "2010", "2011", "2012",
                                         "2013", "2014", "2015"]).rename (columns={"Country Name": "Country"})
    gdp['Country'] = gdp['Country'].replace ({"Korea, Rep.": "South Korea",
                                              "Iran, Islamic Rep.": "Iran",
                                              "Hong Kong SAR, China": "Hong Kong"})

    ScimEn = pd.DataFrame (data_2)

    first_outer_merge_df = pd.merge (ScimEn, energy, how='outer', left_on='Country', right_on='Country')
    second_outer_merge_df = pd.merge (first_outer_merge_df, gdp, how='outer', left_on='Country',
                                      right_on='Country').set_index ("Country")

    first_inner_merge_df = pd.merge (ScimEn, energy, how='inner', left_on='Country', right_on='Country')
    second_inner_merge_df = pd.merge (first_inner_merge_df, gdp, how='inner', left_on='Country',
                                      right_on='Country').set_index ("Country")
    return len (second_outer_merge_df.index) - len (second_inner_merge_df.index)


def answer_three():
    #  Question 3 (6.6%)
    #  What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
    #  This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
    Top15 = answer_one()
    return Top15.iloc[:,10:20].mean(axis=1, skipna = True).sort_values(ascending=False, axis=0)

def answer_four():
   # Question 4 (6.6%)
   # By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
   # This function should return a single number.

    Top15 = answer_one()
    average =answer_three().index[5]
    return Top15

def answer_five():
    #  Question 5 (6.6%)
    #  What is the mean Energy Supply per Capita?
    #  This function should return a single number.

    Top15 = answer_one()
    return Top15["Energy Supply per Capita"].mean()

def answer_six():
    #  Question 6 (6.6%)
    #  What country has the maximum % Renewable and what is the percentage?
    #  This function should return a tuple with the name of the country and the percentage.
    Top15 = answer_one()
    max_renewable = Top15["% Renewable"].max(axis =0)
    max_index_renewable = Top15["% Renewable"].idxmax()
    return (max_index_renewable,max_renewable)

def answer_seven():
    #  Question 7 (6.6%)
    #  Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for
    #  this new column, and what country has the highest ratio?
    #  This function should return a tuple with the name of the country and the ratio.

    Top15 = answer_one()
    Top15["Ratio of Citations"] = Top15["Self-citations"] / Top15["Citations"]
    maximum = Top15["Ratio of Citations"].max(axis=0)
    country = Top15["Ratio of Citations"].idxmax()
    return maximum, country

def answer_eight():
    #  Question 8 (6.6%)
    #  Create a column that estimates the population using Energy Supply and Energy Supply per capita.
    #  What is the third most populous country according to this estimate?
    #  This function should return a single string value.

    Top15 = answer_one()
    Top15["Est. Population"] =(Top15["Energy Supply"]/Top15["Energy Supply per Capita"])
    top_3 = Top15.nlargest(3,"Est. Population").sort_values("Est. Population", ascending=False)
    return top_3.index[-1]

def answer_nine():
   #  Question 9 (6.6%)
   #  Create a column that estimates the number of citable documents per person. What is the correlation between the
   #  number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
   #  This function should return a single number.
   #  (Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)
   Top15 = answer_one ()
   Top15["Est. Population"] = (Top15["Energy Supply"] / Top15["Energy Supply per Capita"])
   Top15['Citable doc per capital'] = Top15['Citable documents'] / Top15['Est. Population']

   return Top15["Citable doc per capital"].corr(Top15['Energy Supply per Capita'], method = "pearson")

def answer_ten():
    #  Question 10 (6.6%)
    #  Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in
    #  the top 15, and a 0 if the country's % Renewable value is below the median.
    #  This function should return a series named HighRenew whose index is the country name sorted in ascending
    #  order of rank.

    Top15 = answer_one()
    median =Top15["% Renewable"].median()
    HighRenew = Top15["% Renewable"].apply(lambda x: 1 if x>=median else 0)
    return HighRenew.sort_values()

def answer_eleven():
    #  Question 11 (6.6%)
    #  Use the following dictionary to group the Countries by Continent, then create a dateframe
    #  that displays the sample size (the number of countries in each continent bin), and the sum, mean,
    #  and std deviation for the estimated population of each country.

# ContinentDict  = {'China':'Asia',
#                   'United States':'North America',
#                   'Japan':'Asia',
#                   'United Kingdom':'Europe',
#                   'Russian Federation':'Europe',
#                   'Canada':'North America',
#                   'Germany':'Europe',
#                   'India':'Asia',
#                   'France':'Europe',
#                   'South Korea':'Asia',
#                   'Italy':'Europe',
#                   'Spain':'Europe',
#                   'Iran':'Asia',
#                   'Australia':'Australia',
#                   'Brazil':'South America'}

    #   This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America',
    #   'South America'] and columns ['size', 'sum', 'mean', 'std']

    Top15 = answer_one()
    ContinentDict  = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}

    Top15["Est. Population"] = (Top15["Energy Supply"] / Top15["Energy Supply per Capita"])
    Top15 = Top15.groupby (ContinentDict)['Est. Population'].agg([("size","count"),("sum","sum"),("mean","mean"),("std","std")])
    return Top15

def answer_twelve():
    pd.get_option ("display.max_columns", 999)
    # Question 12 (6.6%)
    # Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these
    # groups?
    # This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.
    Top15 = answer_one ()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}


    Top15["% Renewable"]= pd.cut(Top15['% Renewable'], 5)
    Top15 = Top15.reset_index()
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    grouped = Top15.groupby(['Continent', '% Renewable'])['Country'].count()
    grouped = grouped.reset_index()
    grouped = grouped.set_index(['Continent', '% Renewable'])
    return grouped['Country']

def answer_thirteen():
    # Question 13 (6.6%)
    # Convert the Population Estimate series to a string with thousands separator (using commas).
    # Do not round the results.
    # e.g. 317615384.61538464 -> 317,615,384.61538464
    # This function should return a Series PopEst whose index is the country name and whose values are the
    # population estimate string.

    Top15 = answer_one()

    Top15["Est. Population"] = (Top15["Energy Supply"] / Top15["Energy Supply per Capita"])
    Top15["Est. Population"] =Top15["Est. Population"].apply(lambda x: '{:,}'.format(x))
    return Top15["Est. Population"]

print(answer_thirteen())

