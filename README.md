# CSDA1050-CAP
	
#Craigslist_Rental
	
	##-> Extraction from API
		ETL from Craigslist done using the Craigslist ETL.py script. This script uses the craigslist library (https://pypi.org/project/python-craigslist/) to pull rental data for the greater toronto area. 

	##-> Transforming/Loading to DB
		The script converts the data recovered to the appropriate data type, separates Geolocation to Lat/Long, separates area (which includes unit on the end) into an integer for area and area unit.
		The script then stores the file in a MS SQL database, connected through a pre established ODBC DSN connection. The DSN connection is established using the ODBC Datasource Administrator tool on Windows. There are no checks for duplicates, this is done in the EDA.

	##-> EDA Notebook
	Overview	
	Checks are done for duplicates and reposts using the post ID. Once identified, these are removed from the dataset. Most of the missing data found are from a first trial data extraction where I opted to drop certian columns (URL, Index, has_image). These missing items have little impact on the rest of the analysis. The notable columns (area, price, lat/lon) are mostly complete. The bedroom data though has a good number of missing values. 

	Findings	
		A variety of metrics are plotted against bedroom count: monthly rent, monthly rent / bedroom, monthly rent / sqft. Notable findings were that the monthly total rent for 3 and 4 bedroom units were quite similar, while the price/bedroom for a 1 bedroom unit is a substantial premium to the remainder of the bedroom options. The most common rental options are 1 and 2 bedroom units by a substantial margin, with the most common area being 750sqft. There was seemingly no correlation between any of the notable factors (price, area, bedrooms, etc). 
		From a geographic analysis of the data, most of the listings were found to be in the downtown core, with the highest price per bedroom generally in that area as well.	
	
	Data Limitations
		The data was from a ~1 month time period, with only data from craigslist being used. Incorporating other site's rental listings (Kijiji, view-it, padmapper, etc), and data from a longer period of time (a full year +) would be better for a more wholistic perspective.
		There is (not yet) definition captured around housing type (basement, house, condo, etc). This would likely have an impact on monthly rent as well.
		The bedroom count (at this point) assumes 1 bedroom and studio apartments to be in the same group. There are also a number of listings with an missing bedroom count, an analysis of the descriptions of these listings would likely establish a better picture.

	##-> Next Steps
	Time permitting I'd plan to take on the below items, in order of priority;
	-Convert maps to MTM and replot (for better visual)
	-Replot the maps with 1,2,3,etc bedroom data separately. 
	-attempt to pull full title and description (using stored listing URLS);
		does sentiment affect rental price?
		is there a way to establish housing type? (basement / condo / house)
		can a bedroom count be inferred? (for missing data and studio vs 1 bedroom)
	-Use OSMnx to attempt to calculate distance to nearest transit stop - have to figure out how to do this
	-Incorporate average income by neighborhood
		census data from https://www12.statcan.gc.ca/wds-sdw/cpr2016-eng.cfm
		census tract to postal code (https://www150.statcan.gc.ca/n1/en/catalogue/92-154-G) - though this seems to be a paid data source now, 
		listing lat/lon to postalcode (need to find resource, maybe this: https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#f71a13c4-fb51-6116-57b7-1f51a8190585)
	-build a model to see if rental price can be predicted given the factors;
		-bedroom
		-Lat/long
		-area
		-listing sentiment
		-average income in area
		-distance to closest transit stop

		-bed