from cgi import test
from email import header
from email.policy import default
import sys
from statistics import mode
from typing_extensions import NotRequired, Required
import click
from matplotlib.pyplot import text
from sqlalchemy import true
import wordcloud
import scraper
from time import sleep
import pandas
import processing
from configparser import ConfigParser,RawConfigParser
import access_sql

@click.group
def cli():
    pass

@click.command()
@click.option('--header/--no-header','-h/-nh', is_flag=True, required=True, prompt="Would you like a header? ", default=True)
@click.option('--sql/--no-sql','-s/-ns', is_flag=True, required=True, prompt="Would you like to upload to the sql database? ", default=False)
@click.option('--file','-f', required=True, prompt=True)
@click.option('--days-ago','-d', required=True, prompt=True, type=int)
@click.option('--interval','-i', required=True, prompt=True, type=int)
@click.option('--query', '-q', required=False, default="(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality)) lang:en -is:retweet")
def past(header, sql, file, interval,days_ago,query):
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
    scraper.exportToFile(data, file, header)
    
@click.command()
@click.option('--header/--no-header','-h/-nh', is_flag=True, required=True, prompt="Would you like a header? ", default=True)
@click.option('--sql/--no-sql','-s/-ns', is_flag=True, required=True, prompt="Would you like to upload to the sql database? ", default=False)
@click.option('--file','-f', required=True, prompt=True)
@click.option('--query', '-q', required=False, default="(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality OR vr OR ar)) lang:en -is:retweet")
def present(header, sql, file,query):
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
        scraper.exportToFile(data, file, header)
        sleeptime = 3570
        for i in range(sleeptime):
            print(f"sleeping for {sleeptime-i} seconds  ", end="\r", flush=True)
            sleep(1)
        

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
@click.option('--text-column', '-c', required=False, type=int, default=1)
def clean(input_file, output_file, text_column):
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data, int(text_column))
    cleaned_text.to_csv("tables/"+ output_file+".csv", index=False)

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
@click.option('--text-column', '-c', required=False, type=int, default=1)
def sentiment(input_file,output_file, text_column):
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data,int(text_column))
    sentiments = processing.get_sentiment_table(cleaned_text, int(text_column))
    sentiments.to_csv("tables/"+ output_file+".csv", index=False)

@click.command()
@click.option('--input-file', '-i', required=True, prompt=True)
@click.option('--output-file', '-o', required=True, prompt=True)
@click.option('--text-column', '-c', required=True, prompt=True, type=int)
@click.option('--extract','-e', required=False, default="")
def freq(input_file, output_file, text_column, extract):
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
@click.option('--text-column', '-c', required=True, prompt=True, type=int)
def word_cloud(input_file, output_file, text_column, width, height, max_words, extract):
    data = pandas.read_csv("tables/"+input_file+".csv")
    cleaned_text = processing.clean_text(data, int(text_column))
    freq = processing.getFreq(cleaned_text,column_row=0, query=extract)
    processing.get_wordcloud(freq,output_file,width,height,int(max_words))

@click.command()
@click.option('--query', '-q', required=False, default="(metaverse (robot OR drone OR virtual reality OR mixed reality OR augmented reality OR vr OR ar)) lang:en -is:retweet")
def run(query):
    header = False
    sql = True
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
        #clean text
        cleaned_text = processing.clean_text(data,int(1))
        data['cleaned_text'] = cleaned_text
        #add sentiment
        sentiments = processing.get_sentiment_table(cleaned_text, int(1))
        data['sentiment'] = sentiments


        #test
        #upload to sql
        data.to_csv("test.csv")
        print("uploading to sql")
        access_sql.uploadToSQL(data)
        
        sleeptime = 3570
        for i in range(sleeptime):
            print(f"sleeping for {sleeptime-i} seconds  ", end="\r", flush=True)
            sleep(1)

cli.add_command(past)
cli.add_command(present)
cli.add_command(clean)
cli.add_command(sentiment)
cli.add_command(freq)
cli.add_command(word_cloud)
cli.add_command(run)

if __name__ == '__main__':
    cli()
    