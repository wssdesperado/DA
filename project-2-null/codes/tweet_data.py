# -------------- scrape_tweet.py --------------
# the location of the twitter dataset
FILE_NAME = '../dataset/tweetid_userid_keyword_sentiments_emotions_United States.csv'
# keys of user information
other_keys = ['tweet_id', 'user_id', 'tweet_timestamp']
# keyword attribute
keyword_key = 'keyword'
keyword_values = ['corona', 'wuhan', 'nCoV', 'covid']
# intensity attribute (values range [0,1])
intensity_keys = ['valence_intensity', 'fear_intensity', 'anger_intensity', 'happiness_intensity',
                  'sadness_intensity']
# sentiment attribute
sentiment_key = 'sentiment'
sentiment_values = ['very negative', 'negative', 'neutral or mixed', 'positive', 'very positive']
# emotion attribute
emotion_key = 'emotion'
emotion_values = ['fear', 'anger', 'happiness', 'sadness', 'no specific emotion']


# -------------- tweet_data.py --------------
# the name of twitter dataset
# FILE_NAME = '../dataset/tweetid_userid_keyword_sentiments_emotions_United States.csv'
# the name of new json file
SAVED_NAME = '../dataset/tweet_like_retweet.json'
# keys in new json file
X_KEYS = ['index', 'tweet_id', 'favorite', 'retweet']
# Twitter API key
consumer_key = 'rYPPzGiUza6y1WqFJoJ5vBkAL'
consumer_secret = 't4ZYifYMOFpXGI00kDcjJ8SUGxvM4zfZROtdXCjaw1iBvxXafl'
access_token = '1439398423728435212-dwcLzZTp9LUD1XaRgxBO8dAX1wsoVD'
access_secret = 'UFI0lichJrRo3Tu7s2ihDG1o8EPFjdCgMOKbK1CkiV3NI'
