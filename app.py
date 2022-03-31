import tweepy
from db import get_woeid
from tokensec import *

auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

def trends_in_string(trnds):
    n = ""
    for i in range(len(trnds)):
        n =n +str(i+1)+'. ' +trnds[i] + '\n'
    return n

def get_tweets(location):
    try:
        trend_place = api.get_place_trends(get_woeid(location)[0])[0]
        trends = trend_place['trends']
        num_of_trends = len(trends)

        l = []
        for i in range(num_of_trends):
            l.append(trends[i]['name'])
        return trends_in_string(l)
    except Exception as ex:
        print(str(ex))
    return 'No tweets Found!'
