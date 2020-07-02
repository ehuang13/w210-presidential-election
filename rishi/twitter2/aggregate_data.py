#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import os
import glob
import re
import pandas as pd
from os import makedirs
from os.path import join, exists
from datetime import datetime, date, timedelta
from pathlib import Path


# In[ ]:





# In[3]:


def get_election_data(start_date, end_date, data_path, file_starts):

    df_all = []
    dayrange = range((end_date - start_date).days + 1)
    
    for daycount in dayrange:
        dt = start_date + timedelta(days=daycount)
        datestr = dt.strftime('%Y_%m_%d')
        fname = join(data_path, file_starts + '_' + datestr + '.csv')
        df_tweet = pd.read_csv(fname)
        
        if len(df_all) == 0:
            df_all = df_tweet
        else:
            df_all = pd.concat([df_all, df_tweet])
            
    return df_all


# In[4]:


def combine_and_save_tweet_files(src_path, target_path, start_date, end_date, year, key_term):
    df_twt = get_election_data(start_date, end_date, src_path, key_term)
    df_twt.to_csv(join(target_path, year + '_' +key_term + '.csv'))
                  


# In[8]:


def agg_all():
    start_dt = datetime.today() - timedelta(days=32)
    end_dt = datetime.today()
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump'), 
                             join('data2','agg','candidate','2020'), 
                             start_dt, end_dt, '2020','trump')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden'), 
                             join('data2','agg','candidate','2020'), 
                             start_dt, end_dt, '2020', 'biden')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_economy'), 
                             join('data2','agg','economy','trump'), 
                             start_dt, end_dt, '2020', 'trump economy')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_economy'), 
                             join('data2','agg','economy','biden'), 
                             start_dt, end_dt, '2020', 'biden economy')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_environment'), 
                             join('data2','agg','environment','trump'), 
                             start_dt, end_dt, '2020', 'trump environment')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_environment'), 
                             join('data2','agg','environment','biden'), 
                             start_dt, end_dt, '2020', 'biden environment')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_republican'), 
                             join('data2','agg','party','trump'), 
                             start_dt, end_dt, '2020', 'trump republican')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_democrat'), 
                             join('data2','agg','party','biden'), 
                             start_dt, end_dt, '2020', 'biden democrat')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_health'), 
                             join('data2','agg','health','trump'), 
                             start_dt, end_dt, '2020', 'trump health')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_health'), 
                             join('data2','agg','health','biden'), 
                             start_dt, end_dt, '2020', 'biden health')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_immigration'), 
                             join('data2','agg','immigration','trump'), 
                             start_dt, end_dt, '2020', 'trump immigration')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_immigration'), 
                             join('data2','agg','immigration','biden'), 
                             start_dt, end_dt, '2020', 'biden immigration')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','trump_job'), 
                             join('data2','agg','job','trump'), 
                             start_dt, end_dt, '2020', 'trump job')
    
    combine_and_save_tweet_files(join('data2','raw','candidate','2020','biden_job'), 
                             join('data2','agg','job','biden'), 
                             start_dt, end_dt, '2020', 'biden job')


# In[5]:





# In[5]:


#combine_and_save_tweet_files(join('data2','raw','candidate','2016','trump'), 
#                             join('data2','agg','candidate','2016'), 
#                             date(2016, 10, 8), date(2016, 11, 7), '2016', 'trump')


# In[7]:


#combine_and_save_tweet_files(join('data2','raw','candidate','2016','hillary'), 
#                             join('data2','agg','candidate','2016'), 
#                             date(2016, 10, 8), date(2016, 11, 7), '2016', 'hillary')


# In[9]:


#combine_and_save_tweet_files(join('data2','raw','candidate','2012','obama'), 
#                             join('data2','agg','candidate','2012','obama'), 
#                             date(2012, 10, 20), date(2012, 11, 4), '2012', 'obama')


# In[11]:


#combine_and_save_tweet_files(join('data2','raw','candidate','2012','romney'), 
#                             join('data2','agg','candidate','2012', 'romney'), 
#                             date(2012, 10, 20), date(2012, 11, 4), '2012', 'romney')

