#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Reference - https://github.com/NLPWM-WHU/TransCap/tree/master/TransCap


# In[1]:


from model import *
from utils import *
from generate_tf_flags import *
import tensorflow as tf

print(tf.__version__)

import numpy as np
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.filterwarnings('ignore')

tf.logging.set_verbosity(tf.logging.ERROR)


# In[2]:


FLAGS = assign_flag_values(tf)


# In[3]:


def main(_):
    start_time = time.time()
    info = ''
    index = 0
    
    for name, value in FLAGS.__flags.items():
        value = value.value
        if index < 19:
            info += '{}:{}  '.format(name, value)
        if index in [5, 11]:
            info += '\n'
        index += 1
    print('\n{:-^80}'.format('Parameters'))
    print(info + '\n')
    
    print('---------')
    print(FLAGS.ASC)
    
    data_path = '../data/{}/'.format(FLAGS.ASC)
    
    if not FLAGS.reuse_embedding :
        print('Initialize Word Dictionary & Embedding')
        word_dict = data_init(data_path, FLAGS.DSC)
        w2v = init_word_embeddings(data_path, word_dict, FLAGS.DSC)
    else:
        print('Reuse Word Dictionary & Embedding')
        with open(data_path + FLAGS.DSC + '_word2id.txt', 'r', encoding='utf-8') as f:
            word_dict = eval(f.read())
        w2v = np.load(data_path + FLAGS.DSC + '_word_embedding.npy')
    
    for i in range(15):
        model = MODEL(FLAGS, w2v, word_dict, data_path)
        model.run()
    
    end_time = time.time()
    print('Running Time: {:.0f}m {:.0f}s'.format((end_time-start_time) // 60, (end_time-start_time) % 60))


# In[4]:


if __name__ == '__main__':
    tf.app.run()


# In[ ]:





# In[ ]:




