# -*- coding: utf-8 -*-
"""
Script for sending a post request to the flask api

"""
import requests
import json
import pandas as pd

#Change the data in this csv file before feeding it in
data = pd.read_csv('transformed_data.csv')

url = 'http://127.0.0.1:5000/predict'
headers = {'Content-type': 'application/json'}
data = {'input': list(data.iloc[0,:].values)} 
res = requests.post(url = url, json = data, headers = headers)

print(res.json())