# -*- coding: utf-8 -*-
"""
This Script is for building a model for the App Rating Predictor Project.
"""
import pandas as pd

data = pd.read_csv('Data_for_Model.csv')

#Label/Target Encode categorical variables
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
enc1 = LabelEncoder()
enc2 = LabelEncoder()
data['Genre'] = enc.fit_transform(data['Genre'])
data['Version'] = enc.fit_transform(data['Version'])
data['Minimum Android Version'] = enc.fit_transform(data['Minimum Android Version'])

#Train Test Split
from sklearn.model_selection import train_test_split
X = data.drop(['Rating'], axis = 1)
y = data['Rating']
X_Train, X_Test, y_train, y_test = train_test_split(X,y, test_size = 0.15, random_state = 0)
X_Train, X_CV, y_train, y_CV = train_test_split(X_Train,y_train, test_size = 0.15, random_state = 0)

X.to_csv('transformed_data.csv', index = False)

#Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
lm = LinearRegression()
lm.fit(X_Train, y_train)
print(mean_absolute_error(y_CV, lm.predict(X_CV)))


#SVR
from sklearn.svm import SVR
svr = SVR()
svr.fit(X_Train, y_train)
print(mean_absolute_error(y_CV, svr.predict(X_CV)))


#Decision Tree Regressor
from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor()
tree.fit(X_Train, y_train)
print(mean_absolute_error(y_CV, tree.predict(X_CV)))


#Random Forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf.fit(X_Train, y_train)
print(mean_absolute_error(y_CV, rf.predict(X_CV)))


#Hyperparameter optimization using GridsearchCV for Boosting models
nums = []
for i in range(20):
    nums.append(0.01 + 0.05*i)
from sklearn.model_selection import RandomizedSearchCV
params1 = {'random_state':range(1,15), 'max_leaves':(8,16,24, 32), 'max_depth': range(1,15), 
          'learning_rate': nums, 'n_estimators': range(10,500,10), 'n_jobs': (4,6),
          'reg_alpha': nums, 'reg_lambda':nums}

params2 = {'random_state':range(1,15), 'num_leaves':(8,16,24, 32), 'max_depth': range(1,15), 
          'learning_rate': nums, 'n_estimators': range(10,500,10), 'n_jobs': (4,6),
          'reg_alpha': nums, 'reg_lambda':nums}

params3 = {'random_state':range(1,15), 'num_leaves':(8,16,24, 32), 'max_depth': range(1,15), 
          'learning_rate': nums, 'n_estimators': range(10,1000,10),
          'reg_lambda':nums}


#XGBoost
from xgboost import XGBRegressor
clf1 = XGBRegressor()
xgb = RandomizedSearchCV(clf1, params1)
xgb.fit(X_Train, y_train, early_stopping_rounds = 5, eval_set = [(X_CV,y_CV)], verbose = False)
print(mean_absolute_error(y_CV, xgb.predict(X_CV)))


#LightGBM
from lightgbm import LGBMRegressor
clf2 = LGBMRegressor()
lgb = RandomizedSearchCV(clf2, params2)
lgb.fit(X_Train, y_train, early_stopping_rounds = 5, eval_set = [(X_CV,y_CV)], verbose = False)
print(mean_absolute_error(y_CV, lgb.predict(X_CV)))


#Catboost
from catboost import CatBoostRegressor
clf3 = CatBoostRegressor()
cat = RandomizedSearchCV(clf3, params3)
cat.fit(X_Train, y_train, early_stopping_rounds = 5, eval_set = [(X_CV,y_CV)], verbose = False)
print(mean_absolute_error(y_CV, cat.predict(X_CV)))


#Model Evaluation
print(mean_absolute_error(y_test, lm.predict(X_Test)))
print(mean_absolute_error(y_test, svr.predict(X_Test)))
print(mean_absolute_error(y_test, tree.predict(X_Test)))
print(mean_absolute_error(y_test, xgb.best_estimator_.predict(X_Test)))
print(mean_absolute_error(y_test, lgb.best_estimator_.predict(X_Test)))
print(mean_absolute_error(y_test, cat.best_estimator_.predict(X_Test)))

import pickle
model = {'lightgbm':lgb.best_estimator_}
pickle.dump(model, open('model_file' + ".p", "wb")) 