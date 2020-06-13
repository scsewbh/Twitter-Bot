# Twitter Bot - Sanjay Sewbhajan
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

#Sanjay Sewbhajan - Giveaway 
#----------------------Settings-------------------------

consumer_key = '---------'
consumer_secret_key = '---------'
access_token = '---------'
access_token_secret = '---------'


#-----------------------Setup---------------------------

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit='True', wait_on_rate_limit_notify='True')
my_id =api.me().id
home_tweets = []
giveaway_tweets = []
current_mentions =[]
c = 0
newest_id_log = [0]

#-------------------Home Page Search---------------------
def home_page_search(api):
    #get home page first //count is number of tweets to pull from timeline
    if c == 0:
        public_tweets = api.home_timeline(count=50, tweet_mode="extended")
        count = 1
    else:
        public_tweets = api.home_timeline(since_id=newest_id_log[0], tweet_mode="extended")


    #iterate between each tweet
    for tweet in public_tweets:
        id = tweet.id
        print(id)
        text = (tweet.full_text).lower()
        print(text)
        if text.startswith('rt @') == True:
            id = tweet.retweeted_status.id
        if text.find('give' or 'like')!=(-1):
            print('1')
            giveaway_tweets.append(id)
            print(text)
            like_comment_retweet(api, id, tweet)
            follow_user_id(api, id, tweet)
        home_tweets.append(id)



    #try and expect to show there is no tweets with giveaway in the first x \\ count=x)
    try:
        newest_id_log[0] = home_tweets[0]
    except IndexError:
        print('No giveaways found')
    except:
        print('Sad Days Boy. No clue what happened to get this error.')
    print ('The newest is: '+ str(newest_id_log))
    return newest_id_log


#------------------------Like----------------------------
def like_tweet(api, id):
    api.create_favorite(id)

#------------------------Comment-------------------------
def comment_on_tweet(api, id, tweet):
    try:
        author_username = '@' + tweet.retweeted_status.user.screen_name
        print('2')
    except:
        author_username = '@' + tweet.user.screen_name
        print('3')

    api.update_status(author_username + ' @SCSKing', id)

#------------------------Retweet-------------------------
def retweet(api, id):
    api.retweet(id)

#----------------------Follow User-----------------------
def follow_user_id(api, id, tweet):
    x = tweet.entities.get('user_mentions')
    for mention in x:
        y = mention.get('id')
        current_mentions.append(y)

    n = api.show_friendship(source_id=my_id,target_id=tweet.user.id)
    if not n[1].following:
        try:
            time.sleep(60)
            api.create_friendship(id=tweet.user.id)
        except:
            time.sleep(15*60)
    else:
        print('Already Following Tweeter')

    try:
        for idnow in current_mentions:
            g = api.show_friendship(source_id=my_id,target_id=idnow)
            if not g[1].following:
                time.sleep(60)
                api.create_friendship(id=idnow)
            else:
                print('Already Following Mention')
    except:
        print('User Mention Empty')

#---------------------Notifications----------------------

#---------------------Multi-Commands---------------------

def like_comment_retweet(api, id, tweet):
    if not tweet.retweeted and not tweet.favorited:
        like_tweet(api, id)
        retweet(api, id)
        comment_on_tweet(api, id, tweet)
    else:
    	print('Already Entered')

#------------------------Main----------------------------
while True:
    print('Before' + str(newest_id_log[0]))
    newest_id_log[0] = home_page_search(api)
    print('After' + str(newest_id_log[0]))
    time.sleep(10*60)


