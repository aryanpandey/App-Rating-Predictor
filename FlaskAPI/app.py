# -*- coding: utf-8 -*-
"""
Script for launching the app
"""
from flask import Flask, request
import json
import pickle
import numpy as np

app = Flask(__name__)

def load_models():
    file_name = 'model/model_file.p'
    with open(file_name, 'rb') as f:
        model = pickle.load(f)
        model = model['lightgbm']
    return model

@app.route('/predict', methods = ['GET','POST']) 
def predict():
    if request.method == 'POST':
        request_json = request.json
        x = request_json['input']
        x = np.array(x).reshape(1,-1)
        model = load_models()
        prediction = model.predict(x)[0]
        #print(prediction)
        response = json.dumps({'Rating': prediction})
        return response, 200
    print('You need to make a post request for this to work!!!')
    return None

if __name__ == '__main__':
    application.run(debug = True)