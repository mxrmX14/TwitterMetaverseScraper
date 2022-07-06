from cgi import test
from email import header
from email.policy import default
import os
import sys
from statistics import mode
from typing_extensions import NotRequired, Required
import click
from matplotlib.pyplot import text
from sqlalchemy import true
import wordcloud
import twitter_scraper.scripts.scraper as scraper
from time import sleep
import pandas
import twitter_scraper.scripts.processing as processing
from configparser import ConfigParser,RawConfigParser
import twitter_scraper.scripts.access_sql as access_sql

@click.group
def cli():
    pass

@click.command()
@click.option('--header/--no-header','-h/-nh', is_flag=True, required=True, prompt="Would you like a header? ", default=True)
@click.option('--output-file','-o', required=True, prompt=True)
@click.option('--days-ago','-d', required=True, prompt=True, type=int)
@click.option('--interval','-i', required=True, prompt=True, type=int)
@click.option('--query', '-q', required=False, default="(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality)) lang:en -is:retweet")
def past(header, output_file, interval,days_ago,query):
    bearerToken = scraper.readConfig()
    tweets = scraper.grab_tweets_past(bearerToken=bearerToken, query=query, days_ago=days_ago, interval=interval)
    data = pandas.DataFrame({
        "created_at": [],
        "tweet_text": [],
        "id": [],
        "author_id": [],
        "retweet_count": [],
        "reply_count":  [],
        "like_count": [],
        "quote_count": [],
        "followers_count": [],
        "following_count": [],
        "tweet_count": [],
        "verified": [],
        "account_created":[],
        "username": [],
        "account_location": [],
        "bio": [],
        "location": []
        })
    data = data.append(tweets)
    scraper.exportToFile(data, output_file, header)
    
@click.command()
@click.option('--header/--no-header','-h/-nh', is_flag=True, required=True, prompt="Would you like a header? ", default=True)
@click.option('--output-file','-o', required=True, prompt=True)
@click.option('--query', '-q', required=False, default="(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality OR vr OR ar)) lang:en -is:retweet")
def present(header, output_file,query):
    bearerToken = scraper.readConfig()
    while True:
        tweets = scraper.grab_tweets_now(bearerToken=bearerToken, query=query)
        data = pandas.DataFrame({
            "created_at": [],
            "tweet_text": [],
            "id": [],
            "author_id": [],
            "retweet_count": [],
            "reply_count":  [],
            "like_count": [],
            "quote_count": [],
            "followers_count": [],
            "following_count": [],
            "tweet_count": [],
            "verified": [],
            "account_created":[],
            "username": [],
            "account_location": [],
            "bio": [],
            "location": []
            })
        data = data.append(tweets)
        scraper.exportToFile(data, output_file, header)
        sleeptime = 3570
        for i in range(sleeptime):
            print(f"sleeping for {sleeptime-i} seconds  ", end="\r", flush=True)
            sleep(1)
        

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
def clean(input_file, output_file):
    text_column = 1
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data, int(text_column))
    cleaned_text.to_csv("tables/"+ output_file+".csv", index=False)

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
def sentiment(input_file,output_file):
    text_column = 1
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data,int(text_column))
    sentiments = processing.get_sentiment_table(cleaned_text, int(text_column))
    sentiments.to_csv("tables/"+ output_file+".csv", index=False)

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
@click.option('--extract','-e', required=False, default="")
def freq(input_file, output_file, extract):
    text_column = 1
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data, int(text_column))
    freq = processing.getFreq(cleaned_text,column_row=0, query=extract)
    
    freq.to_csv("tables/"+ output_file+".csv", header=False)

@click.command()
@click.option('--extract','-e', required=False, default="")
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
@click.option('--width', '-h', required=False, default=1600)
@click.option('--height', '-w', required=False, default=800)
@click.option('--max-words', '-m', required=False, default=1000, type=int)
def word_cloud(input_file, output_file, width, height, max_words, extract):
    text_column = 1
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tables/'+input_file+'.csv'))
    data = pandas.read_csv(filepath)
    cleaned_text = processing.clean_text(data, int(text_column))
    freq = processing.getFreq(cleaned_text,column_row=0, query=extract)
    processing.get_wordcloud(freq,output_file,width,height,int(max_words))

@click.command()
@click.option('--output-file', '-o', required=True, prompt=True)
def get_table(output_file):
    access_sql.export(output_file)
    

cli.add_command(past)
cli.add_command(present)
cli.add_command(clean)
cli.add_command(sentiment)
cli.add_command(freq)
cli.add_command(word_cloud)
cli.add_command(get_table)

if __name__ == '__main__':
    cli()
    