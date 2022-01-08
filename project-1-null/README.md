# COSC-587-P1

This is your starter repo for Project 1. You will find the assignment
and the example cheatsheet. 

Files:
Project1.pdf
API-cheatsheet.py

### File project_1_report.pdf is our final report for project-1

## COVID ACT NOW API

api resource: https://apidocs.covidactnow.org/

### how to run the code: 

run ./codes/covid_act_now_api.py
        
### output:

1)the code will output a dict of the fraction of missing values for each attribute in console

2)the code will generate a file named "results.csv", which contains the dataset - each row contains one-day data in a specific state

## COVID Rest API for MongoDB covid dataset

api resource: https://www.mongodb.com/developer/article/johns-hopkins-university-covid-19-rest-api/

### output:

1)RestAPI.py the code will output a series of txt files of covid information

2)MongoDB_cleaniness.py the code will output a cleaned data 

## THE COVID TRACKING PROJECT API

api resource: https://covidtracking.com/data/api

### how to run the code: 

run ./codes/COVID_Tracking_API.py

./codes/COVID_Tracking_API_Data.py is the key and defined parameters used by COVID_Tracking_API.py.
### output:

1)the code will output the count of null numbers and number error(number should not be negative is negatice) in states and US.
  the code will output the count of null numbers of some important variables and fraction of it with total number in states and US.

2)if uncomment lines 100-102,the code will generate three files named "States_Daily.json", "States_Info.json", "US_Daily.json" which contains the dataset - each row contains one-day data in a specific state/whole US.There files also have been submitted in folder "dataset", so comment these lines won't affect the code run.

## The Twitter COVID Dataset

data resource: https://www.openicpsr.org/openicpsr/project/120321/version/V10/view?path=/openicpsr/120321/fcr:versions/V10/Twitter-COVID-dataset---Sep2021/tweetid_userid_keyword_sentiments_emotions_United-States.csv.zip&type=file

### decription:

The data is too large to upload on github. Therefore, we provide an url on Google drive. If you can't download it successfully, contact us.(you can still try to download the data from the data resource above.)
url:https://drive.google.com/file/d/1tZ2qp3S_GmU0tIHN3Q9VtehjPexrTWnS/view?usp=sharing

### how to run the code:

run ./codes/tweet_clean.py

### output:

1)tweet_clean.py: code are used to measure the cleanliness level of the Twitter-COVID-dataset
2)tweet_data.py：contain parameters used in the two python files (tweet_clean.py and scrape_tweet.py) .

## The Tweet Like Retweet Dataset

data resource:  ./dataset/tweet_like_retweet.json

### decription:

It contains 4 attributes 'index', 'tweet_id', 'favorite', 'retweet'
Data comes from scrape_tweet.py, but the file is not the whole data we scraped. 
On account of the lack of server and the unstability of the author's home network, it takes lots of time to scrape data from twitter, so we just upload the first 5000 data in github. We will upload the whole data later.

### how to run the code:

run ./codes/scrape_tweet.py

### output:

scrape_tweet.py: code are used to scrape the “favorite” and “retweet” of tweets. Tweet ID comes from the Twitter-COVID-dataset
