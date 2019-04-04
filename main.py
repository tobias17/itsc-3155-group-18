import tweepy
import numpy as np
from textblob import TextBlob

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)
#
# for tweet in tweets:
#     phrase = TextBlob(tweet.text)
