# -*- coding: utf-8 -*-
"""
This Script is for building a model for the App Rating Predictor Project.
"""
import numpy as np
import pandas as pd
import gensim
import logging
from gensim.models import Word2Vec
import pickle
import nltk
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import f1_score, mean_squared_error, accuracy_score
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
#nltk.download('punkt')

data = pd.read_csv('../Data/play_store_data.csv')
drop_list = ['analysis_split', 'description', 'developerAddress', 'histogram', 'inAppProductPrice', 'installs',
             'recentChanges', 'summary','editorsChoice', 'free', 'minInstalls',
             'price', 'ratings', 'reviews', 'contentRatingDescription', 'title']

#Get minimum Age Rating
def get_min_age(entry):
    if entry == entry:
        entry = int(entry.split(' ')[-1][:-1])
    else:
        entry = 0
        
    return entry

data['min_age_rating'] = data['contentRating'].apply(get_min_age)
drop_list.append('contentRating')

#Fill Missing Values
text_columns = ['currency', 'developer', 'genre', 'title']
num_columns = ['Day', 'Month', 'Year', 'androidVersion', 'containsAds', 'Years_from_release',
               'minInstalls', 'offersIAP', 'originalPrice', 'size', 'product_price', 'min_age_rating']

data[text_columns] = data[text_columns].fillna('Missing')
data[num_columns] = data[num_columns].fillna(-1)

data = data[data['score'].notna()]

'''Get Word Vector Representations for all Textual Columns
wv = gensim.models.KeyedVectors.load_word2vec_format('../Data/GoogleNews-vectors-negative300.bin', binary=True)
wv.init_sims(replace=True)
def word_averaging(wv, words, counter):
    all_words, mean = set(), []
    
    for word in words:
        if isinstance(word, np.ndarray):
            mean.append(word)
        elif word in wv.vocab:
            mean.append(wv.syn0norm[wv.vocab[word].index])
    
    if not mean:
        counter += 1
        return np.zeros(wv.vector_size,)
    
    mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0).astype(np.float32))
    return mean

def word_averaging_list(wv, text_list, counter=0):
    return np.vstack([word_averaging(wv, post, counter) for post in text_list]), counter

def w2v_tokenize_text(text):
    tokens = []
    try:
        for sent in nltk.sent_tokenize(text, language ='english'):
            for word in nltk.word_tokenize(sent, language = 'english'):
                if len(word) < 2:
                    continue
                tokens.append(word)
    except:
        tokens.append('Other')
    return tokens

def pca(w2v, components=5, var=None):
    pca = PCA(n_components=components)
    pca.fit(w2v)
    a = pd.DataFrame(pca.transform(w2v), columns=['pca_{}_{}'.format(i,var) for i in range(0, components)])
    data[a.columns] = a
    
title_tokenized = data['title'].apply(lambda x:" ".join(i for i in x)).astype(str).apply(lambda r:w2v_tokenize_text(r)).values
title_w2v, counter = word_averaging_list(wv, title_tokenized)
print("Could not compute similarity for ", str(counter), " items")
pca(title_w2v, components=5, var='Title')

data.drop(['title'], axis = 1, inplace = True)
#'''
#Drop a few Columns
data.drop(drop_list, axis = 1, inplace = True)


#Label/Target Encode categorical variables
def label_encode(df, var, minority_limit):
    minor_groups = df[var].value_counts()[df[var].value_counts()<minority_limit].index
    
    replace_list = []
    for i in range(0, len(minor_groups)):
        replace_list.append('other')
        
    df[var] = df[var].replace(minor_groups, replace_list)
    
    le = LabelEncoder()
    df[var] = le.fit_transform(df[var])
    
    with open('../Model_Data/le_'+var+'.pkl', 'wb') as f:
        pickle.dump(le, f)
    
minority_limits = {'currency':3, 'developer':1, 'genre':120}

for i in text_columns[:-1]:
    label_encode(data, i, minority_limits[i])

#'''
def bin_score(entry):
    if entry>4.5:
        return 4
    elif entry>4:
        return 3
    elif entry>3:
        return 2
    elif entry>1.75:
        return 1
    else:
        return 0
    
data['score'] = data['score'].apply(bin_score)
#'''
#XGBoost
data.dropna(inplace=True)
X = data.drop(['score'], axis = 1)
Y = data['score']


kfold = StratifiedKFold(n_splits = 5, shuffle = True, random_state = 42)

splits = kfold.split(X, Y)
acc_scores = []
weighted_scores = []

from xgboost import XGBClassifier, XGBRegressor

for i, (Train, Test) in enumerate(splits):
    X_Train, X_Test, Y_Train, Y_Test = X.iloc[Train], X.iloc[Test], Y.iloc[Train], Y.iloc[Test]
    
    sm = SMOTE(random_state = 42, n_jobs = -1)
    X_Train, Y_Train = sm.fit_resample(X_Train, Y_Train)
    
    xgb = XGBClassifier(n_estimators = 2000, n_jobs = -1, learning_rate = 0.1, reg_lambda = 0.1, objective = 'multiclassova')
    xgb.fit(X_Train, Y_Train, early_stopping_rounds = 100, eval_set = [(X_Train, Y_Train), (X_Test, Y_Test)], eval_metric = 'mlogloss',  verbose = False)
    
    with open('../Model_Data/model_'+str(i)+'.pkl', 'wb') as f:
        pickle.dump(xgb, f)
    
    pred = xgb.predict(X_Test)
    
    acc_scores.append(accuracy_score(Y_Test, pred))
    weighted_scores.append(f1_score(Y_Test, pred, average = 'weighted'))
    
#print("RMSE:", mean_squared_error(Y_CV, pred, squared = False))
#'''
print("Weighted F1:", sum(weighted_scores)/len(weighted_scores))
print("Accuracy:", sum(acc_scores)/len(acc_scores))
#'''