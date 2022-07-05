import pandas 
import re
from nltk.stem.snowball import SnowballStemmer
import nltk

import matplotlib.pyplot as plt
from nltk.probability import FreqDist
import numpy as np
import seaborn as sns
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path

def getFreq(data_frame, column_row):
    text_column = data_frame[str(data_frame.columns[column_row])]

    word_list = []

    for text in text_column:
        for word in text:
            if word not in nltk.corpus.stopwords.words('english'):
                word_list.append((word))


    frequency = {}
    for item in word_list:
        if item in frequency:
            frequency[item] +=1
        else: 
            frequency[item] = 1
    return frequency





## uncomment to save to csv

#////---------------------------------------------------//////////
final = pandas.DataFrame.from_dict(wordFreq, orient='index')


wordcloud = WordCloud(width=1600,height=800, max_words=1000).generate_from_frequencies(imageType)

print('what would you like the image name to be?')
imageName = str(input())
wordcloud.to_file("img/"+imageName+".png")

print("done!")


