#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pycorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')


# In[4]:


nlp = StanfordCoreNLP('http://localhost:9000')


# In[5]:


def get_sentiment(text):
    res = nlp.annotate(text,
                       properties={'annotators': 'sentiment',
                                   'outputFormat': 'json',
                                   'timeout': 1000,
                       })
    
    try:
        if len(res['sentences']) == 0:
            return -1
        else:
            return res['sentences'][0]['sentimentValue']
    except:
        return False
    else:
        return -1


# In[6]:


def clean_tweets(tw):
    
    stopWords = set(stopwords.words('english'))
    if tw in stopWords:
        return ''
    
    return tw


# In[7]:


def get_scores(df):
    
    scores = []
    
    counter = 0
    
    for index, row in df.iterrows():
        if isinstance(row['text'], str):
            
            row['text'] = clean_tweets(row['text'])
            row['text'] = row['text'].lower()
            score = int(get_sentiment(row['text']))
            if score != -1:
                scores.append(score)
            else:
                scores.append(2)
            
        else:
            scores.append(2)
            
        counter += 1
        
        if counter % 1000 == 0:
            print(counter)

    df['scores'] = scores
    
    return df


# In[8]:


def get_and_save_sentiments(src_path, target_path):
    
    df_tweet = pd.read_csv(src_path)
    df_score = get_scores(df_tweet)
    df_score.to_csv(target_path)


# In[12]:


def generate_all_sentiments():
    
    print('---- candidate ------')

    get_and_save_sentiments('data2/agg/candidate/2020/2020_trump.csv',
                           'data2/sentiment/candidate/2020/2020_trump.csv')
    
    get_and_save_sentiments('data2/agg/candidate/2020/2020_biden.csv',
                       'data2/sentiment/candidate/2020/2020_biden.csv')
    
    #get_and_save_sentiments('data2/agg/candidate/2016/trump/2016_trump.csv',
    #                   'data2/sentiment/candidate/2016/trump/2016_trump.csv')
    
    #get_and_save_sentiments('data2/agg/candidate/2016/hillary/2016_hillary.csv',
    #                   'data2/sentiment/candidate/2016/hillary/2016_hillary.csv')
    
    #get_and_save_sentiments('data2/agg/candidate/2012/obama/2012_obama.csv',
    #                   'data2/sentiment/candidate/2012/obama/2012_obama.csv')
    
    #get_and_save_sentiments('data2/agg/candidate/2012/romney/2012_romney.csv',
    #                   'data2/sentiment/candidate/2012/romney/2012_romney.csv')
    
    print('---- economy ------')
    
    get_and_save_sentiments('data2/agg/economy/trump/2020_trump economy.csv',
                       'data2/sentiment/economy/trump/2020_trump economy.csv')
    
    get_and_save_sentiments('data2/agg/economy/biden/2020_biden economy.csv',
                       'data2/sentiment/economy/biden/2020_biden economy.csv')
    
    print('---- party ------')
    
    get_and_save_sentiments('data2/agg/party/trump/2020_trump republican.csv',
                       'data2/sentiment/party/trump/2020_trump republican.csv')
    
    get_and_save_sentiments('data2/agg/party/biden/2020_biden democrat.csv',
                       'data2/sentiment/party/biden/2020_biden democrat.csv')
    
    print('---- environment ------')
    
    get_and_save_sentiments('data2/agg/environment/trump/2020_trump environment.csv',
                       'data2/sentiment/environment/trump/2020_trump environment.csv')
    
    get_and_save_sentiments('data2/agg/environment/biden/2020_biden environment.csv',
                       'data2/sentiment/environment/biden/2020_biden environment.csv')
    
    print('---- health ------')
    
    get_and_save_sentiments('data2/agg/health/trump/2020_trump health.csv',
                       'data2/sentiment/health/trump/2020_trump health.csv')
    
    get_and_save_sentiments('data2/agg/health/biden/2020_biden health.csv',
                       'data2/sentiment/health/biden/2020_biden health.csv')
    
    
    print('---- immigration ------')
    
    get_and_save_sentiments('data2/agg/immigration/trump/2020_trump immigration.csv',
                       'data2/sentiment/immigration/trump/2020_trump immigration.csv')
    
    get_and_save_sentiments('data2/agg/immigration/biden/2020_biden immigration.csv',
                       'data2/sentiment/immigration/biden/2020_biden immigration.csv')
    
    
    print('---- job ------')
    
    get_and_save_sentiments('data2/agg/job/trump/2020_trump job.csv',
                       'data2/sentiment/job/trump/2020_trump job.csv')
    
    get_and_save_sentiments('data2/agg/job/biden/2020_biden job.csv',
                       'data2/sentiment/job/biden/2020_biden job.csv')

