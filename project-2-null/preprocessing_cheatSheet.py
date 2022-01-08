#############################
# Data Preprocessing
# Examples using pandas and movie data set
#
# Version 1
#############################

import numpy as np
import pandas as pd
from pprint import pprint


# Array to hold data
myData = []

dataFile = open("movie_data.csv", encoding='latin1')

# Read data into array
line = dataFile.readline()
while (line):
	if line.endswith('\n'):
               #remove the new line symbol from the line 
    	    line = line[:-1]
	myData.append(line)
	line = dataFile.readline()

dataFile.close()
pprint("\nReading array")
pprint(myData)

# Read in data directly into pandas
myDataFrame = pd.read_csv('movie_data.csv' , sep=',', encoding='latin1')

print("\n\nData Frame format")
pprint(myDataFrame)

# Print first 3 rows
print("\n\nData Frame first three rows")
pprint(myDataFrame[:3])

# Print 'title' column
print("\n\nData Frame title")
pprint(myDataFrame['title'])

# Print first 5 rows of genres
print("\n\nData Frame first 5 rows of Genres")
pprint(myDataFrame['genres'][:5])

# Print the first 5 rows of budget and revenues
print("\n\nData Frame budget and revenue")
pprint(myDataFrame[['budget', 'revenue']][:5])

# See the count of each value for release dates
dateCounts = myDataFrame['release_date'].value_counts()
print("\n\nRelease date Counts")
pprint(dateCounts)

# Determine which rows having title with 'Mad' in the title
madRows = myDataFrame[myDataFrame['title'].str.contains('Mad', na=False, case=False)]
# spaceRows = df[df['title'].str.contains('mad')]
print("\n\nSongs with the word 'mad' in the title")
pprint(madRows['title'])

# Count all the rows with a value from the list
valueList = ['Chris Columbus', 'Clint Eastwood', 'Michael Bay']
rowsWithDirector = myDataFrame["director"].isin(valueList)
count = rowsWithDirector.sum()
print("\n\nCount of Directors in list: " + str(count))

# Unique year list
yearList = pd.unique(myDataFrame["release_year"])
print("\n\nUnique releaes year List")
pprint(yearList)

#####################
# Clean & Organize the data
#####################

# Make song titles upper case
myDataFrame['title'] = myDataFrame['title'].str.upper()
print("\n\nUpper Case")
pprint(myDataFrame[:10])

# Delete a column from the dataframe
del myDataFrame['cast']
print("\n\nRemove column")
pprint(myDataFrame[:10])

# Iterate through data frame
print("\n\nIterate through")
for index, row in myDataFrame.iterrows():
        print(index, row['title'])

# Sort data by multiple columns
myDataFrame = myDataFrame.sort_values(by=['budget','revenue', 'release_year'])
pprint(myDataFrame[:10])

# Write the data to a file
myFileName="out.csv"
myDataFrame.to_csv(myFileName)



