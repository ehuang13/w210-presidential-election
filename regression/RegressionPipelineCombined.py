#!/usr/bin/env python
# coding: utf-8

# In[184]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report


# In[185]:


pd.set_option('max_columns', None)


# In[186]:


combined_data_file = "../../data/Data-Jul16/combined_jul16.csv"
data_2020_file = "../../data/Data-Jul16/F20_jul05.csv"
data_historical = pd.read_csv(combined_data_file, encoding = "ISO-8859-1")


# In[187]:


data_2020 = pd.read_csv(data_2020_file, encoding = "ISO-8859-1")
data_2016 = data_historical.loc[data_historical['YEAR'] == 2016]
data_2012 = data_historical.loc[data_historical['YEAR'] == 2012]
data_2008 = data_historical.loc[data_historical['YEAR'] == 2008]

year_df_dict = {2020:data_2020, 2016:data_2016, 2012:data_2012, 2008:data_2008}


# In[188]:


data_historical['COUNTY_TOTALVOTES'] = data_historical['COUNTY_TOTALVOTES'].astype(np.int64)


# ### PrepData###

# In[189]:


data_historical['REP_VOTES%'] = data_historical['REP_VOTES'] / data_historical['COUNTY_TOTALVOTES']
data_historical['DEM_VOTES%'] = data_historical['DEM_VOTES'] / data_historical['COUNTY_TOTALVOTES']
data_2020['REP_VOTES%'] = data_2020['REP_VOTES'] / data_2020['COUNTY_TOTALVOTES']
data_2020['DEM_VOTES%'] = data_2020['DEM_VOTES']/ data_2020['COUNTY_TOTALVOTES']


# In[190]:


data_historical.drop(['REP_VOTES', 'DEM_VOTES'], axis=1, inplace=True)
data_2020.drop(['REP_VOTES', 'DEM_VOTES'], axis=1, inplace=True)


# In[191]:


data_historical.drop(['WINNING_CANDIDATE', 'WINNING_PARTY_BINARY', 'REP_CANDIDATE', 'DEM_CANDIDATE', 'WINNING_PARTY', 'COUNTY', 'STATE', 'REP_VOTES%', 'DEM_VOTES%', 'MARGIN_VICTORY'], axis=1, inplace=True)


# In[192]:


def train_test_split_by_year(X, y, year, cols=None):
    
    if year != None:
        year_filter =  X['YEAR'] < year
        X = X[year_filter]
        y = y[year_filter]
        
    X = X.drop('YEAR', axis=1)
    y = np.delete(y, 1, axis=1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    if (cols == None):
        return X_train, X_test, y_train, y_test
    else:
        return X_train[cols], X_test[cols], y_train, y_test


# # Step 1 #

# ### Build/Train Model#1: Linear regression to preidct total votes by county###
# 

# In[193]:


year = 2016
target_df = year_df_dict.get(year)


# In[194]:


X = data_historical.drop(['COUNTY_TOTALVOTES'], axis=1)
y = data_historical[['COUNTY_TOTALVOTES', 'YEAR']].values


# In[195]:


X_train, X_test, y_train, y_test = train_test_split_by_year(X, y, year)


# In[196]:


linear_model = LinearRegression()


# In[197]:


linear_model.fit(X_train, y_train)


# In[198]:


y_pred = linear_model.predict(X_test)


# In[199]:


print("Accuracy score={:.2f}".format(linear_model.score(X_test, y_test) * 100))


# ### Generate Total Votes Predictions by County###

# In[200]:


target_df.drop(['COUNTY_TOTALVOTES'], inplace=True, axis=1, errors='ignore')


# In[201]:


target_df.drop(['ID', 'YEAR', 'Unnamed: 0', 'Unnamed: 0.1', 'WINNING_CANDIDATE', 'WINNING_PARTY_BINARY', 'REP_CANDIDATE', 'DEM_CANDIDATE', 'WINNING_PARTY', 'COUNTY', 'STATE', 'REP_VOTES%', 'DEM_VOTES%', 'REP_VOTES', 'DEM_VOTES', 'COUNTY_TOTALVOTES', 'MARGIN_VICTORY'], axis=1, inplace=True, errors='ignore')


# In[202]:


y_pred_target = linear_model.predict(target_df)


# In[203]:


#merge predictions with the target dataset. 
target_df['COUNTY_TOTALVOTES'] = y_pred_target


# In[204]:


target_df['COUNTY_TOTALVOTES'] = target_df['COUNTY_TOTALVOTES'].astype(np.int64)


# In[205]:


import datetime

x = datetime.datetime.now()
day = x.day
month = x.month

date_str = str(month) + str(day)


# In[206]:


#save file (will be used by next step in the pipeline)
filename_step1 = '../../data/F20_step1_output_' + date_str + '.csv'
target_df.to_csv(filename_step1)


# # Step 2 #

# In[207]:


# start clean and reimport everything again. 
data = pd.read_csv(combined_data_file, encoding = "ISO-8859-1")


# In[208]:


data_2020 = pd.read_csv(data_2020_file, encoding = "ISO-8859-1")
data_2016 = data.loc[data['YEAR'] == 2016]
data_2012 = data.loc[data['YEAR'] == 2012]
data_2008 = data.loc[data['YEAR'] == 2008]


# ### Build/Train Model#2: Random Forest Classifier to predict County Winner###

# In[209]:


data.drop(['REP_VOTES', 'DEM_VOTES', 'MARGIN_VICTORY', 'WINNING_CANDIDATE', 'REP_CANDIDATE', 'DEM_CANDIDATE', 'WINNING_PARTY', 'COUNTY', 'STATE'], axis=1, inplace=True)
data.drop(['AA_FEMALE', 'AA_MALE', 'BA_FEMALE', 'BA_MALE', 'H_FEMALE', 'H_MALE', 'IA_FEMALE', 'IA_MALE', 'NA_FEMALE', 'NA_MALE' , 'TOT_FEMALE', 'TOT_MALE', 'TOT_POP', 'WA_FEMALE', 'WA_MALE', 'TOT_POP_LESS19', 'TOT_MALE_LESS19', 'TOT_FEMALE_LESS19', 'TOT_POP_20to39', 'TOT_MALE_20to39', 'TOT_FEMALE_20to39', 'TOT_POP_40to59', 'TOT_MALE_40to59', 'TOT_FEMALE_40to59', 'TOT_POP_Above60', 'TOT_MALE_Above60', 'TOT_FEMALE_Above60'] , axis=1, inplace=True)


# In[210]:


significant_cols = [
 'STATE_FIPS',
 'COUNTY_FIPS',
 'COUNTY_TOTALVOTES',
 'HOUSE_WINNING_BINARY',
 'SENATE_WINNING_BINARY',
 'UNEMPLOYMENT_RATE',
 'AVG_WAGE_SALARY',
 'BA_FEMALE%',
 'BA_MALE%',
 'H_FEMALE%',
 'IA_FEMALE%',
 'WA_FEMALE%',
 'WA_MALE%',
 'TOT_FEMALE%',
 'TOT_MALE%',
 'TOT_POP_LESS19%',
 'TOT_POP_40to59%',
 'TOT_POP_Above60%']


# In[211]:


X = data.drop('WINNING_PARTY_BINARY', axis=1)
y = data[['WINNING_PARTY_BINARY', 'YEAR']].values

X_train, X_test, y_train, y_test = train_test_split_by_year(X, y, year, significant_cols)


# In[212]:


rfc4 = RandomForestClassifier(n_estimators=10).fit(X_train, y_train)

rfc_pred4= rfc4.predict(X_test)

print("Experiment#rfc4: {:.3f}%".format(accuracy_score(y_test, rfc_pred4) * 100))


# In[213]:


print(classification_report(y_test, rfc_pred4))


# ### Predict County winner ###

# In[214]:


target_year_data = pd.read_csv(filename_step1, encoding = "ISO-8859-1")


# In[215]:


## use with significant model only..
## for now drop AVG_WAGE_SALARY till data is fixed. 
data_significant = target_year_data[[
 'STATE_FIPS',
 'COUNTY_FIPS',
 'COUNTY_TOTALVOTES',
 'HOUSE_WINNING_BINARY',
 'SENATE_WINNING_BINARY',
 'UNEMPLOYMENT_RATE',
 'AVG_WAGE_SALARY',
 'BA_FEMALE%',
 'BA_MALE%',
 'H_FEMALE%',
 'IA_FEMALE%',
 'WA_FEMALE%',
 'WA_MALE%',
 'TOT_FEMALE%',
 'TOT_MALE%',
 'TOT_POP_LESS19%',
 'TOT_POP_40to59%',
 'TOT_POP_Above60%']]


# In[216]:


y_pred = rfc4.predict(data_significant)


# In[217]:


target_year_data['WINNING_PARTY_BINARY'] = y_pred


# In[218]:


#save to csv
filename_step2 = '../../data/F20_step2_output_' + date_str + '.csv'
target_year_data.to_csv(filename_step2)


# # Step 3

# ### Build/Train Model#3: Linear Regression to predict R/D Votes for every county###

# In[222]:


votes_historcail_df = pd.read_csv(combined_data_file, encoding = "ISO-8859-1")
votes_df = pd.read_csv(filename_step2)


# In[223]:


votes_historcail_df_copy = votes_historcail_df[['YEAR','STATE_FIPS', 'COUNTY_FIPS', 'COUNTY_TOTALVOTES', 'WINNING_PARTY_BINARY', 'REP_VOTES']]


# In[224]:


votes_historcail_df_copy['REP_VOTES%'] = votes_historcail_df_copy['REP_VOTES'] / votes_historcail_df_copy['COUNTY_TOTALVOTES']
votes_historcail_df_copy.drop('REP_VOTES', axis=1, inplace=True)


# In[225]:


X = votes_historcail_df_copy.drop(['REP_VOTES%'], axis=1)
y = votes_historcail_df_copy[['REP_VOTES%', 'YEAR']].values


# In[226]:


X_train, X_test, y_train, y_test = train_test_split_by_year(X, y, year)


# In[228]:


linear_model = LinearRegression()
linear_model.fit(X_train, y_train)


# In[229]:


y_pred = linear_model.predict(X_test)


# In[230]:


print("Accuracy score={:.2f}".format(linear_model.score(X_test, y_test) * 100))


# In[231]:


from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


# ### Predict R and D Total votes per County###

# In[232]:


votes_df_copy = votes_df[['STATE_FIPS', 'COUNTY_FIPS', 'COUNTY_TOTALVOTES', 'WINNING_PARTY_BINARY']]


# In[233]:


y_pred = linear_model.predict(votes_df_copy)


# In[234]:


target_year_data['REP_VOTES%'] = y_pred


# In[235]:


#info D total votes. 
target_year_data['DEM_VOTES%'] = 1 - target_year_data['REP_VOTES%']


# In[236]:


target_year_data['REP_VOTES'] = target_year_data['REP_VOTES%'] * target_year_data['COUNTY_TOTALVOTES']
target_year_data['DEM_VOTES'] = target_year_data['DEM_VOTES%'] * target_year_data['COUNTY_TOTALVOTES']


# In[237]:


target_year_data['REP_VOTES'] = target_year_data['REP_VOTES'].astype(np.int64)
target_year_data['DEM_VOTES'] = target_year_data['DEM_VOTES'].astype(np.int64)


# In[238]:


#save to csv
filename_step3 = '../../data/F20_step3_output_' + date_str + '.csv'
target_year_data.to_csv(filename_step3)


# # Step 4

# ### Calculate Winner###

# In[239]:


electoral_ref = pd.read_excel('../../data/Electoral College Votes.xlsx')
target_data = pd.read_csv(filename_step3)
data_historical = pd.read_csv(combined_data_file, encoding = "ISO-8859-1")


# In[240]:


### 1) create a new df with StateFips/Count
state_fips_map = {}
for index, row in data_historical.iterrows():
    #print(row)
    state = row['STATE']
    #print(type(state))
    if (state_fips_map.get(state) == None):
        state_fips_map[state] = row['STATE_FIPS']
        
state_fips_df = pd.DataFrame(list(state_fips_map.items()), columns=['STATE','STATE_FIPS'])


# In[241]:


df = electoral_ref.merge(state_fips_df, left_on='STATE', right_on='STATE')


# In[242]:


target_data.drop('Unnamed: 0', inplace=True, axis=1)


# In[244]:


"""extract how counties prediction for every state"""
visited = {}
electoral_votes = {'D':0, 'R':0 }
for idnex, row in target_data.iterrows():
    state = int(row['STATE_FIPS'])
    
    rep_votes = int(row['REP_VOTES'])
    dem_votes = int(row['DEM_VOTES'])

    if (visited.get(state) == None):
        electoral_votes = {'D': dem_votes, 'R': rep_votes }
        visited[state] = electoral_votes
    else:
        #update existing map
        current_votes = visited.get(state)
        current_r = current_votes.get('R')
        current_d = current_votes.get('D')
        electoral_votes = {'D': current_d + dem_votes, 'R': current_r + rep_votes }
        visited[state] = electoral_votes


# In[245]:


"""determine the winner of every state"""
state_predictions = {}
d_count = 0
r_count = 0

for key, val in visited.items():
    total_r = val.get('R')
    total_d = val.get('D')
    winner = 'D' if total_d > total_r else 'R'
    
    if (winner == 'D'):
        d_count +=1 
    elif (winner == 'R'):
        r_count +=1
    
    state_predictions[key] = winner

# In[246]:


party_electoral = {}
for index, row in df.iterrows():
    state = int(row['STATE_FIPS'])
    votes = int(row['COUNT'])
    party = state_predictions.get(state)
    
    if (party_electoral.get(party) == None):
        party_electoral[party] = votes
    else:
        new_total = party_electoral.get(party) + votes
        party_electoral[party] = new_total


# In[247]:


# Print Summary #
print('======== SUMMARY ========')
print('r=' + str(r_count))
print('d=' + str(d_count))
print(party_electoral)
print('=========================')

# In[ ]:




