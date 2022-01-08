#############################
# Examples using APIs
#
# Version 1
#############################

import requests

# Define variables
data = []
zip_code = "22152"

# Setup parameters for API query
base_url = "http://www.airnowapi.org/aq/forecast/zipCode/"
query_params = {"API_KEY":"ADD YOUR KEY",
				"format":"application/json",
				"distance":25}
query_params["zipCode"] = zip_code	# Set zip code to current input value

# Query AirNowAPI for AQI data using input zip codes as parameters
response = requests.get(base_url, query_params)

# Pull out the json text
json_txt = response.json()

# Select columns of interest from json text [NOTE json libary does this in a nice way]
for record in json_txt:

	# Use .get() because some results don't have data for all attributes
	d = [record.get("DateIssue"),
	record.get("DateForecast"),
	record.get("ReportingArea"),
	record.get("StateCode"),
	record.get("Latitude"),
	record.get("Longitude"),
	record.get("ParameterName"),
	record.get("AQI"),
	record.get("Category").get("Number"),
	record.get("Category").get("Name"),
	record.get("ActionDay"),
	record.get("Discussion")]

	data.append(d)

# Print header and data
headers= ["DateIssue", "DateForecast", "ReportingArea", "StateCode",
			  "Latitude", "Longitude", "ParameterName", "AQI",
			  "CategoryNumber", "CategoryName", "ActionDay", "Discussion"]
print(headers)
print(data)
