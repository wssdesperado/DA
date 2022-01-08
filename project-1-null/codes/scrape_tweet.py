#############################
# Create a new json file containing favorites and retweets from Tweepy
# We collect the tweet_id from Twitter-COVID-dataset, and then scrape the number of favorites and retweets
# new json file 'tweet_like_retweet.json'
#
# Version 1
#############################
from tweepy import OAuthHandler, TweepError
import json
import pandas as pd
import tweepy
from tweet_data import *
import numpy as np


# Scrape favorites and retweets from Tweepy
def get_data():
    # Read data using pandas
    df = pd.read_csv(FILE_NAME, encoding="latin1")

    # Get tweet_id column and convert it into a list
    tweet_ids = df["tweet_id"].to_list()
    print("GET DATA SUCCESSFULLY!")

    # Authenticate Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    i = 1
    delete_count = 0  # number of tweets which are deleted and cannot found
    index = []  # index of data
    favorite = []  # number of favorite in each tweet
    retweet = []  # number of retweet in each tweet
    tweetId = []  # the id of each tweet

    print("Start Scraping...")
    for id in tweet_ids:
        # Scrape tweet data for the first tweet_ID
        try:
            # get the information of tweet
            tweetFetched = api.get_status(id)
        except TweepError:
            # catch error if the tweet has been deleted.
            delete_count = delete_count + 1
        else:
            # save attributes
            index.append(i)
            tweetId.append(id)
            favorite.append(tweetFetched.favorite_count)
            retweet.append(tweetFetched.retweet_count)
        finally:
            i = i + 1
            # print process
            if i % 100 == 0:
                print(i)
            # if i == 5000:
            #     break
    # save information in dict
    tweet = {}
    tweet['index'] = index
    tweet['tweet_id'] = tweetId
    tweet['favorite'] = favorite
    tweet['retweet'] = retweet
    # print(tweet)
    print('total data:', i - 1)
    print('delete count:', delete_count)
    return tweet


# read the saved data if needed
def read_file(FILE_NAME):
    with open(FILE_NAME) as f:
        input = json.load(f)
        X = []
        for key in input.keys():
            if key in X_KEYS: X.append(input[key])
        f.close()
    return X


if __name__ == '__main__':
    # get data
    data = get_data()
    # save data in json file
    with open(SAVED_NAME, 'w') as file_obj:
        json.dump(data, file_obj)
    print("JSON SAVED SUCCESSFULLY!")

    # # read the saved data if needed
    # X = read_file(SAVED_NAME)
    # print(X)
    # print(len(X))
    # X = np.transpose(np.array(X))
    # print('--------INPUT INFO-----------')
    # print("X shape:", X.shape)


