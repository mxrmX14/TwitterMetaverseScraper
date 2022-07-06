from email.quoprimime import quote
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from fileinput import filename
import tweepy
import pandas
import numpy as np
from datetime import datetime
from datetime import timedelta
import os
from time import sleep
from configparser import RawConfigParser

def readConfig():
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'authentication/'+'config.ini'))
    config = RawConfigParser()
    config.read(filepath)
    bearerToken = str(config['tokens']['bearer'])
    return bearerToken

def grab_tweets_now(bearerToken, query):

    #client for tweepy
    client = tweepy.Client(bearerToken, wait_on_rate_limit=True)

    #sets the start time to grab tweets
    begin = (datetime.today() + timedelta(hours=5) - timedelta(hours=1)).isoformat("T") + "Z"
    end = (datetime.today() +timedelta(hours=5) - timedelta(seconds=30)).isoformat("T") + "Z"

    # grabs tweets, returns "tweet" object
    result = client.search_recent_tweets(
            query=query,
            max_results = 100,
            start_time = begin,
            tweet_fields = "public_metrics,author_id,created_at", 
            user_fields = "public_metrics,verified,username,created_at,description,location",
            end_time = end,
            expansions = "author_id"
            )

    #lists for columns
    created_at = []
    text = []
    id = []
    author_id = []
    retweet_count = []
    reply_count = []
    like_count = []
    quote_count = []
    followers_count = []
    following_count = []
    tweet_count = []
    verified = []
    account_created =[]
    username = []
    account_location = []
    bio = []
    location = []

    users = {u["id"]: u for u in result.includes['users']}

    #adds items to a list 
    for j in result.data:
        
        created_at.append(j.created_at)
        text.append(j.text)
        id.append(j.id)
        author_id.append(j.author_id)
        retweet_count.append(j.public_metrics["retweet_count"])
        reply_count.append(j.public_metrics["reply_count"])
        like_count.append(j.public_metrics["like_count"])
        quote_count.append(j.public_metrics["quote_count"])
        location.append(j.geo)

        if users[j.author_id]:
            user = users[j.author_id]
            followers_count.append(user.public_metrics["followers_count"])
            following_count.append(user.public_metrics["following_count"])
            tweet_count.append(user.public_metrics["tweet_count"])
            verified.append(user.verified)
            account_created.append(user.created_at)
            username.append(user.username)
            account_location.append(user.location)
            bio.append(user.description)

    #makes dataFrame with lists
    df = pandas.DataFrame({
        "created_at": created_at,
        "tweet_text": text,
        "id": id,
        "author_id": author_id,
        "retweet_count": retweet_count,
        "reply_count":  reply_count,
        "like_count": like_count,
        "quote_count": quote_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "tweet_count": tweet_count,
        "verified": verified,
        "account_created": account_created,
        "username": username,
        "account_location": account_location,
        "bio": bio,
        "location": location
        })

    return df

def grab_tweets_past(bearerToken, query, days_ago, interval):
    #client for tweepy
    client = tweepy.Client(bearerToken, wait_on_rate_limit=True)

    #sets the start time to grab tweets
    startTime = datetime.today()

    #lists for columns
    created_at = []
    text = []
    id = []
    author_id = []
    retweet_count = []
    reply_count = []
    like_count = []
    quote_count = []
    followers_count = []
    following_count = []
    tweet_count = []
    verified = []
    account_created =[]
    username = []
    account_location = []
    bio = []
    location = []

    
    for i in range(int((days_ago*24)/interval)):
        begin = (startTime - timedelta(days=days_ago) + timedelta(hours=5) - timedelta(seconds=0)).isoformat("T") + "Z"
        end = (startTime - timedelta(days=days_ago) + timedelta(hours=5) + timedelta(hours=interval))
        if (end <= (startTime+timedelta(hours=5))):
            end = (startTime - timedelta(days=days_ago) + timedelta(hours=5) + timedelta(hours=interval) - timedelta(seconds=10)).isoformat("T") + "Z"
        else: 
            end = (startTime - timedelta(days=days_ago) + timedelta(hours=5) + timedelta(hours=interval) - timedelta(seconds=0)).isoformat("T") + "Z"
        
        # grabs tweets, returns "tweet" object
        result = client.search_recent_tweets(
            query=query,
            max_results = 100,
            start_time = begin,
            tweet_fields = "public_metrics,author_id,created_at", 
            user_fields = "public_metrics,verified,username,created_at,description,location",
            end_time = end,
            expansions = "author_id"
            )


        users = {u["id"]: u for u in result.includes['users']}

        #adds items to a list 
        for j in result.data:
            
            created_at.append(j.created_at)
            text.append(j.text)
            id.append(j.id)
            author_id.append(j.author_id)
            retweet_count.append(j.public_metrics["retweet_count"])
            reply_count.append(j.public_metrics["reply_count"])
            like_count.append(j.public_metrics["like_count"])
            quote_count.append(j.public_metrics["quote_count"])
            location.append(j.geo)

            if users[j.author_id]:
                user = users[j.author_id]
                followers_count.append(user.public_metrics["followers_count"])
                following_count.append(user.public_metrics["following_count"])
                tweet_count.append(user.public_metrics["tweet_count"])
                verified.append(user.verified)
                account_created.append(user.created_at)
                username.append(user.username)
                account_location.append(user.location)
                bio.append(user.description)
        

        print("grabbed tweets ("+str(i)+"/"+str(int((days_ago*24)/interval)-1)+")")

        startTime += timedelta(hours=interval)
     

    #makes dataFrame with lists
    df = pandas.DataFrame({
        "created_at": created_at,
        "tweet_text": text,
        "id": id,
        "author_id": author_id,
        "retweet_count": retweet_count,
        "reply_count":  reply_count,
        "like_count": like_count,
        "quote_count": quote_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "tweet_count": tweet_count,
        "verified": verified,
        "account_created": account_created,
        "username": username,
        "account_location": account_location,
        "bio": bio,
        "location": location
    
        })

    return df

def exportToFile(data, filename,header):
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'tables/'+filename+'.csv'))
    data.to_csv(filepath, mode='a', header=header, index=False)
    print("exported")
