import tweepy
import numpy as np
from textblob import TextBlob


def is_english(text):
    if text.detect_language() == "en":
        return True
    return False

def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)

    polarities = []
    subjectivities = []
    for tweet in tweets:
        phrase = TextBlob(tweet.text)

        if not is_english(phrase):
            phrase = TextBlob(str(phrase.translate(to="en")))

        if phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0:
            polarities.append(phrase.sentiment.polarity)
            subjectivities.append(phrase.sentiment.subjectivity)


consumer_key = "3TpaZaHD3Z6LDfA0Ytj8xlmn8"
consumer_secret = "zVV3K0eynOPV8rrwF4Tq996nYNX5HaJsHUS5QZZXwkV4nCI6l8"

access_token = "1113877575280070660-a7X4ZsQEZ6yophra9nAgaL7wg0BFCF"
access_token_secret = "2meYVBvWjvg4aF8fz8zNXyGAN28hUMkwFlVcfts0vzujg"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print ("authenticated")

query = "Coke"
tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)
for tweet in tweets:
    phrase = TextBlob(tweet.text)
    print(phrase)
print ("searched")
