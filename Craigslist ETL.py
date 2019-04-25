#%%
#load library and class
from craigslist import CraigslistHousing
import pandas as pd
import numpy as np
import sqlalchemy

#%%
#establish query, then seek results
cl = CraigslistHousing(site='toronto', area='tor', category='apa')
results = cl.get_results(sort_by='newest', geotagged=True, limit= 3000)

#Store results in a vector for easier referencing and analysis
listings = []

for result in results:
    listings.append(result)

#Print off top 3 to see dataset
print (listings[:3])
#%%

#Convert JSON to Dataframe
df = pd.DataFrame.from_records(listings)

#replace "None" with NA
df.fillna(value=np.NAN, inplace=True)
df['geotag']=np.where(df['geotag'] =='nan', np.NAN, df['geotag'])


#drop unnecessary columns
#cols = [4,5,10]
#df.drop(df.columns[cols], axis=1, inplace=True)

#Remove unit of measurement from area column and store separately. 
#Checking where imperial or metric units are used and consolodating to imperial
#%%
df['area_measure'] = df['area'].str[-3:]
df['area'] = df['area'].str[:-3]
df.area_measure.unique()
#%%

#Split Lat and Long into separate columns
lat = []
lon = []

#remove leading and lagging brackets
df['geotag'] = df['geotag'].map(lambda x: str(x)[1:-1],na_action='ignore')

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
#Convert Numeric Columns
df.area = df['area'].astype(str).astype(float)
df.bedrooms = df['bedrooms'].astype(str).astype(float)
df.id = df['id'].astype(str).astype(float)
df.latitude = df['latitude'].astype(str).astype(float)
df.longitude = df['longitude'].astype(str).astype(float)
df.repost_of = df['repost_of'].astype(str).astype(float)

    #remove "$" from price, then convert to float
df['price'] = df['price'].str[1:]
df.price = df['price'].astype(str).astype(float)

#Convert datetime to datetime
df['datetime']=pd.to_datetime(df['datetime'])
#%%

#write to csv
#df.to_csv('CL472019.csv',index=False)


engine = sqlalchemy.create_engine("mssql+pyodbc://USER:password@DETSQL")
df.to_sql('CSDA1050_CL', con=engine, if_exists='append')

