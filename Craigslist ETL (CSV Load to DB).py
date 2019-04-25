# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 14:50:14 2019

@author: mParravani

This script loads the CSV file first pulled into the database.
"""

import pandas as pd
import numpy as np
import sqlalchemy
import pymssql
import pyodbc



#%%
#load in CSV file (from first data pull)
df = pd.read_csv('CL.csv')
print(df.head())
list(df)

#%%

#Load in data from database - to conform all column headers
myQuery = "SELECT TOP 5 * FROM dbo.CSDA1050_CL"
engine = sqlalchemy.create_engine("mssql+pyodbc://USER:PASSWORD@DETSQL")

df_db = pd.read_sql_query(myQuery, engine)



#%%

#I deleted some columns in the first data pull, and now need to create dummy columns so i can append the CSV file into the database
#Create empty columns where df from CSV file doesn't have columns. 

tmp = list(df_db)


for colname in list(df_db):
    if colname not in list(df):
        df[colname] = np.NAN
#%%

#Transform geotag into lat/long  

df.loc[df.geotag=="a", 'geotag'] = np.nan

      
lat = []
lon = []
        
# For each row in a varible,
for row in df['geotag']:
    # Try to,
    try:
        # Split the row by comma and append
        # everything before the comma to lat
        lat.append(row.split(',')[0])
        # Split the row by comma and append
        # everything after the comma to lon
        lon.append(row.split(',')[1])
    # But if you get an error
    except:
        # append a missing value to lat
        lat.append(np.NaN)
        # append a missing value to lon
        lon.append(np.NaN)

# Create two new columns from lat and lon
df['latitude'] = lat
df['longitude'] = lon

#%%
#Are the two sets of column names equal?
sorted(list(df)) == sorted(list(df_db))
#yes - now load into MSSQL

#%%
df.area = df['area'].astype(str).astype(float)
df.bedrooms = df['bedrooms'].astype(str).astype(float)
df.id = df['id'].astype(str).astype(float)
df.latitude = df['latitude'].astype(str).astype(float)
df.longitude = df['longitude'].astype(str).astype(float)
df.repost_of = df['repost_of'].astype(str).astype(float)
df.geotag = df['geotag'].astype(str)
#df.has_image = df['has_image'].astype(str).astype(bool)
df.has_map = df['has_map'].astype(str).astype(bool)
df.url = df['url'].astype(str)


df['price'] = df['price'].str[1:]
df.price = df['price'].astype(str).astype(float)
df['datetime']=pd.to_datetime(df['datetime'])

#%%

engine = sqlalchemy.create_engine("mssql+pyodbc://USER:PASSWORD@DETSQL")
df.to_sql('CSDA1050_CL', con=engine, if_exists='append',index=False)

#%%