# -*- coding: utf-8 -*-
"""
Script for launching the app
"""
import flask
from flask import Flask, jsonify, request
import json
import pickle

app = Flask(__name__)

def load_models():
    file_name = 'model/model_file.p'
    with open(file_name, 'rb') as f:
        model = pickle.load(f)
        model = model['lightgbm']
    return model

@app.route('/predict') 
def predict():
    request_json = request.get_json()
    x = float(request_json['input'])
    model = load_models()
    prediction = model.predict(x)[0]
    response = json.dumps({'Prediction': prediction})
    return response, 200

if __name__ == '__main__':
    application.run(debug = True)