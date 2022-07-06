from email import header
from operator import index
import pandas 
import re
import os
from nltk.stem.snowball import SnowballStemmer
import nltk
import twitter_scraper.scripts.sentimentProcessing as sentimentProcessing

import matplotlib.pyplot as plt
from nltk.probability import FreqDist
import numpy as np
import seaborn as sns
from PIL import Image
from sqlalchemy import column
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path

def extract_extra(text_dataframe, column):

    #takes the dataframe and turns it into one column
    text_column = text_dataframe[str(text_dataframe.columns[column])]

    #creates 2 dataframe to export both hashtags and mentions
    Hashtags = pandas.DataFrame(index=[0], columns=["hashtags"])
    Mentions = pandas.DataFrame(index=[0], columns=["mentions"])

    for i in range(len(text_column)):
            
        #for every pair of text in the colum it extracts mentions and hashtags
        hashtag_list = list(re.findall(r'(?i)\#\w+', text_column[i]))
        Hashtags.loc[i,"hashtags"] = hashtag_list
        mentions_list = list(re.findall(r'(?i)\@\w+', text_column[i]))
        Hashtags.loc[i,"mentions"] = mentions_list

    return Hashtags,Mentions
        
def clean_text(text_dataframe,column):

    #creates a text column
    text_column = text_dataframe[str(text_dataframe.columns[1])]

    #creates a dataframe to export
    text = pandas.DataFrame(index=[0], columns=["text"])

    for i in range(len(text_column)):
        #for every pair of text in the column, it takes away mentions, hashtags, and links
        text_iteration = str(text_column[i])
        text_iteration = re.sub(r'(?i)\#\w+', ' ', text_iteration)
        text_iteration = re.sub(r'(?i)\@\w+', ' ', text_iteration)
        text_iteration = re.sub(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', ' ', text_iteration)
        text_iteration = re.sub(r'[^\w\s]', '', text_iteration)

        
        #appends the text to dataframe
        text.loc[i,"text"] = text_iteration

    #returns text in dataframe
    return text

def get_sentiment_table(sentiment_dataframe, column):

    
    #takes clean dataframe and takes the text column
    sentiment_text = sentiment_dataframe[str(sentiment_dataframe.columns[0])]

    #sets and creates dataframe to put sentiments
    sentiment_table = pandas.DataFrame(index=[0],columns=["sentiment"])

    #for every pair of text in the column 
    for i in range(len(sentiment_text)):

        #analyzes sentiment and appends it to the table
        sentiment = sentimentProcessing.analyze_sentiment(sentiment_text[i])
        sentiment_table.loc[i,"sentiment"] = sentiment
        print(f"Done with {i} sentiment with {sentiment} score  ", end='\r', flush=True)
    
    return sentiment_table

def getFreq(data_frame, column_row, query):
    # takes the text column
    text_column = data_frame[str(data_frame.columns[column_row])]

    #sets the list of words
    word_list = []
    #for every pair of text in the column
    for i in range(len(text_column)):
        #for every text in the column lowercase it and split it
        text = text_column[i]
        text = text.lower()
        text = text.split()
        #for every word in the string thats not a stopword, add it to the dictionary
        for word in text:
            if word not in nltk.corpus.stopwords.words('english'):
                word_list.append((word))

    #clean query
    query_text = re.sub(r'[^\w\s]', '', query)
    query_text = re.sub(r'(OR)', '', query_text)
    query_text = query_text.split()

    
    frequency = {}
    for item in word_list:
        if item not in query_text:
            if item in frequency:
                frequency[item] +=1
            else: 
                frequency[item] = 1
    
    final = pandas.DataFrame.from_dict(frequency, orient='index')
    
    #return dataframe of the frequencys
    return final

def get_wordcloud(frequency, image_name, width, height, max_words):
    freq_dict = pandas.DataFrame.to_dict(frequency)
    wordcloud = WordCloud(width=width,height=height, max_words=max_words).generate_from_frequencies(freq_dict[0])

    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'img/'+image_name+'.png'))
    wordcloud.to_file(filepath)
