# -*- coding: utf-8 -*-
"""
This Script is for building a model for the App Rating Predictor Project.
"""
import numpy as np
import pandas as pd
import gensim
import logging
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import f1_score, mean_squared_error, accuracy_score
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

data = pd.read_csv("../Data/play_store_data.csv")
drop_list = [
    "analysis_split",
    "description",
    "developerAddress",
    "histogram",
    "inAppProductPrice",
    "installs",
    "recentChanges",
    "summary",
    "editorsChoice",
    "free",
    "minInstalls",
    "price",
    "ratings",
    "reviews",
    "contentRatingDescription",
    "title",
]

# Seggregating the apps based on number of ratings, because lesser number of ratings can influence behaviour
data = data[data["ratings"] > 100]

# New Feature: Average Score of the apps made by the developer previously


# Get minimum Age Rating
def get_min_age(entry):
    if entry == entry:
        entry = int(entry.split(" ")[-1][:-1])
    else:
        entry = 0

    return entry


data["min_age_rating"] = data["contentRating"].apply(get_min_age)
drop_list.append("contentRating")

# Fill Missing Values
text_columns = ["currency", "developer", "genre", "title"]
num_columns = [
    "Day",
    "Month",
    "Year",
    "androidVersion",
    "containsAds",
    "Years_from_release",
    "minInstalls",
    "offersIAP",
    "originalPrice",
    "size",
    "product_price",
    "min_age_rating",
]

data[text_columns] = data[text_columns].fillna("Missing")
data[num_columns] = data[num_columns].fillna(-1)

data = data[data["score"].notna()]

# Drop a few Columns
data.drop(drop_list, axis=1, inplace=True)


# Label/Target Encode categorical variables
def label_encode(df, var):

    le = LabelEncoder()
    df[var] = le.fit_transform(df[var])

    with open("../Model_Data/le_" + var + ".pkl", "wb") as f:
        pickle.dump(le, f)


for i in text_columns[:-1]:
    label_encode(data, i)

#'''
def bin_score(entry):
    if entry > 4.75:
        return 8
    elif entry > 4.6:
        return 7
    elif entry > 4.4:
        return 6
    elif entry > 4.2:
        return 5
    elif entry > 4:
        return 4
    elif entry > 3.75:
        return 3
    elif entry > 3.5:
        return 2
    elif entry > 2:
        return 1
    else:
        return 0


data["score"] = data["score"].apply(bin_score)
#'''
# XGBoost
data.dropna(inplace=True)
X = data.drop(["score"], axis=1)
print(X.columns)
Y = data["score"]

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

splits = kfold.split(X, Y)
acc_scores = []
weighted_scores = []

from lightgbm import LGBMClassifier

for i, (Train, Test) in enumerate(splits):
    X_Train, X_Test, Y_Train, Y_Test = (
        X.iloc[Train],
        X.iloc[Test],
        Y.iloc[Train],
        Y.iloc[Test],
    )

    sm = SMOTE(random_state=0, n_jobs=-1)
    X_Train, Y_Train = sm.fit_resample(X_Train, Y_Train)

    xgb = LGBMClassifier(
        n_estimators=2000, n_jobs=-1, learning_rate=0.1, reg_lambda=0.1
    )
    xgb.fit(
        X_Train,
        Y_Train,
        early_stopping_rounds=100,
        eval_set=[(X_Train, Y_Train), (X_Test, Y_Test)],
        verbose=True,
    )

    with open("../Model_Data/model_" + str(i) + ".pkl", "wb") as f:
        pickle.dump(xgb, f)

    pred = xgb.predict(X_Test)

    acc_scores.append(accuracy_score(Y_Test, pred))
    weighted_scores.append(f1_score(Y_Test, pred, average="weighted"))

# print("RMSE:", mean_squared_error(Y_CV, pred, squared = False))
#'''
print("Weighted F1:", sum(weighted_scores) / len(weighted_scores))
print("Accuracy:", sum(acc_scores) / len(acc_scores))
#'''
