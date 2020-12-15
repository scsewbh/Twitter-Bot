# Twitter Bot
#-------------------------------------
# Limits:
# Follow Limit 
# 400 - New following per day
# 300 - tweets or retweets every 3 hours
# 1000 - likes per day
# 1000 - DMs sent per day
#-------------------------------------

import requests
import json
import time
import tweepy
from random import seed
from random import randint

#----------------------Settings-------------------------
#Destroyer Account
consumer_key = ''
consumer_secret_key = ''
access_token = ''
access_token_secret = ''

tweet = [' Bye. ']
link = 'Chicken.'

users_viewed = []

#-----------------------Setup---------------------------

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit='True', wait_on_rate_limit_notify='True')
my_id = api.me().id
seed(1)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        id = status.id
        try:
            author_username = '@' + status.retweeted_status.user.screen_name
        except:
            author_username = '@' + status.user.screen_name
        if author_username in users_viewed:
            pass
        else:
            users_viewed.append(author_username)
            value = randint(0,6)
            api.update_status(author_username + tweet[value] + link, id)
            timer = randint(600,1800)
            time.sleep(timer)

    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

'''
def delete_my_timeline(api):
    my_tweets = api.user_timeline(my_id, count=10)

    #iterate between each tweet
    for tweet in my_tweets:
        id = tweet.id
        print(id)

        try:
            api.destroy_status(id)
        except:
            api.unretweet(id)


delete_my_timeline(api)
'''

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['merry'], is_async=True)