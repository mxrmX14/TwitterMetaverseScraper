from email.quoprimime import quote
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from sqlalchemy import create_engine

import mysql.connector
import pymysql
from fileinput import filename
import tweepy
import pandas
import numpy as np
from datetime import datetime
from datetime import timedelta
from time import sleep
from configparser import ConfigParser,RawConfigParser

# def main():
#     query = "(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality)) lang:en -is:retweet"
#     data = pandas.DataFrame({
#         "created_at": [],
#         "tweet_text": [],
#         "id": [],
#         "author_id": [],
#         "retweet_count": [],
#         "reply_count":  [],
#         "like_count": [],
#         "quote_count": [],
#         "followers_count": [],
#         "following_count": [],
#         "tweet_count": [],
#         "verified": [],
#         "account_created":[],
#         "username": [],
#         "account_location": [],
#         "bio": [],
#         "location": []
#         })
#     bearerToken = readConfig()

#     filename, days_ago, interval, past, header, upload = prompt()

#     if (past):
#         df = grab_tweets_past(bearerToken, query, days_ago, interval, upload)
        
#         if upload: 
#             uploadToSQL(df)
#         data = data.append(df)
#         exportToFile(data, filename, header)
#     else:
#         while True:
#             df = grab_tweets_now(bearerToken, query, upload)
#             exportToFile(df, filename, header)
#             sleep(3570)


