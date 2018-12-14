import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def create_dict_from_csv(csv):
    '''creates a dictionary of topics for each city
    inputs:
        csv(string)
    returns:
    dictionary
    '''

    df = pd.read_csv(csv)
    zm_mex = pd.read_csv('zmmex.csv')[['CVE_MUN', 'MUN']]
    cities = list(set(zm_mex['MUN']))
    paired_cities= []
    for x, y in zip(list(df['Unnamed: 0']), cities):
        pair = (x,y)
        paired_cities.append(pair)
    diction={}
    ls=[]
    for index,row in df.iterrows():
        temp_list=[]
        if row[1]=='No topics found':
            ls.append('NO TEXT')
        else:
            a = (row[1].split("),"))
            d= {}
            for element in a:
                a = element.replace('\'',"")
                a = a.replace("[","")
                a = a.replace("(","")
                a = a.replace(")]","")
                a = a.split(',')
                key='Topic'+''+ str(a[0])
                values = a[1:]
                temp_list.append(a)
                d[key]=values
            for city in paired_cities:
                if index==city[0]:
                    diction[city[1]] = d
    return diction

def create_str(dict_of_topics,topic):
    '''Creates a string with all the words in a topic
    input:
        dictionary (dict): dictionary of cities and n_topics
        topic (String): valid topics. Valid values are ["Topic1", "Topic 2", "Topic 3",
        Topic 4, Topic 5]
    returns:
        string'''
    list_of_words = []
    for dictionary in list((dict_of_topics.values())):
        list_of_words.extend((dictionary[topic]))
        list_of_words=list(set(list_of_words) - set('ad'))
    big_string = " ".join(list_of_words)
    return big_string

def create_word_cloud(dictionary,topic, num_words, background):
    '''creates a wordcloud object showing the most important words by topic
    inputs:
        dictionary: dictionary of topics and cities
        topic: topic which words are displayed
        num_words: maximum number of words
        background: background of the wordcloud
    returns:
        display an image'''
    wordcloud = WordCloud(max_words=num_words, background_color=background).generate(create_str(dictionary, topic))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
