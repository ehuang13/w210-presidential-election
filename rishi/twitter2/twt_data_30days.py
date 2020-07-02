#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
from datetime import datetime, date, timedelta

import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect
import glob
import os


# In[2]:


from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results


# In[3]:


premium_search_args = load_credentials("creds_twitter_keys.yaml",
                                       yaml_key="search_tweets_premium",
                                       env_overwrite=False)


# In[ ]:





# In[4]:


def get_tweets(search_words, start_date, end_date, num_twt):
    rule = gen_rule_payload(search_words,
                        from_date=start_date.strftime("%Y-%m-%d"),
                        to_date=end_date.strftime("%Y-%m-%d"),
                        results_per_call=num_twt)
    
    tweets = collect_results(rule, max_results=num_twt, result_stream_args=premium_search_args)
    
    tweets_col_filter = [[tweet['created_at'], tweet['text'], tweet['id'], tweet['user']['id'], 
                tweet['user']['location'], tweet['user']['followers_count'], tweet['user']['lang'], 
                tweet['user']['time_zone'], tweet['retweet_count'], tweet['favorite_count']
               ] 
               for tweet in tweets]
    
    tweet_df = pd.DataFrame(data=tweets_col_filter, 
                    columns=['created_at', 'text', 'id', 'user_id', 'user_loc', 'user_followers', 'user_lang',
                            'user_time_zone', 'retweet_count', 'fav_count'])
    
    
    return tweet_df


# In[5]:


def save_tweets(tweet_df, start_date, sub_dir, search_key):
    timestampStr = start_date.strftime("%Y_%m_%d")
    
    tweet_df.to_csv('data2/raw/candidate/2020/' + sub_dir + '/' + search_key + '_' + timestampStr + '.csv')


# In[6]:


def get_and_save_twts_by_day(start_date, sub_dir, search_str, num_days):
    
    for d in range(num_days):
        end_date = start_date + timedelta(days=1)
        #search_str = 'trump OR biden'
        num_twt = 500

        tweet_df = get_tweets(search_str, start_date, end_date, num_twt)
        save_tweets(tweet_df, start_date, sub_dir, search_str)

        print(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        print(len(tweet_df))

        start_date = start_date + timedelta(days=1)
    


# In[33]:


def get_twt_data_today():
    td = datetime.today() #- timedelta(days=1)
    
    get_and_save_twts_by_day(td, 'trump', 'trump', 1)
    get_and_save_twts_by_day(td, 'biden', 'biden', 1)
    
    get_and_save_twts_by_day(td, 'trump_economy', 'trump economy', 1)
    get_and_save_twts_by_day(td, 'biden_economy', 'biden economy', 1)
    
    get_and_save_twts_by_day(td, 'trump_environment', 'trump environment', 1)
    get_and_save_twts_by_day(td, 'biden_environment', 'biden environment', 1)
    
    get_and_save_twts_by_day(td, 'trump_health', 'trump health', 1)
    get_and_save_twts_by_day(td, 'biden_health', 'biden health', 1)
    
    get_and_save_twts_by_day(td, 'trump_immigration', 'trump immigration', 1)
    get_and_save_twts_by_day(td, 'biden_immigration', 'biden immigration', 1)
    
    get_and_save_twts_by_day(td, 'trump_job', 'trump job', 1)
    get_and_save_twts_by_day(td, 'biden_job', 'biden job', 1)
    
    get_and_save_twts_by_day(td, 'trump_republican', 'trump republican', 1)
    get_and_save_twts_by_day(td, 'biden_democrat', 'biden democrat', 1)
    


# In[5]:





# In[ ]:




