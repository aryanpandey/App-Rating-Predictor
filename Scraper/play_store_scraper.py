# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

['NEW_FREE','NEW_PAID', 'TOP_FREE', 'TOP_PAID',
            'TOP_GROSSING', 'TRENDING']
['ANDROID_WEAR', 'ART_AND_DESIGN']

,'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
's','t','u','v','w','x','y','z'
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import time

url = 'https://play.google.com'

driver = webdriver.Chrome(executable_path = r'C:/Projects/App-Downloads-Predictor/Scraper/chromedriver.exe')

driver.implicitly_wait(2)
driver.maximize_window()
driver.get(url +'/store/apps')
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
           's','t','u','v','w','x','y','z']
hrefs =[]
for i in letters:
    driver.find_element_by_name('q').send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    driver.find_element_by_name('q').send_keys(i)
    time.sleep(1)
    driver.find_element_by_class_name('gbqfb').click()
    time.sleep(2.5)
    app = driver.find_elements_by_class_name('poRVub')
    for j in range(len(app)):
        hrefs.append(app[j].get_attribute('href'))

app_data = pd.DataFrame()
print(len(np.unique(np.asarray(hrefs))))
print('test')
c = 0
links = np.unique(np.asarray(hrefs))
for i in links:
    driver.get(i)
    time.sleep(0.5)
    
    print('{}\r'.format(c), end = " ")
    c = c + 1
    
    try:
        rating = driver.find_element_by_class_name('BHMmbe').text
    except:
        rating = -1
    try:
        Number_reviews = driver.find_element_by_class_name('EymY4b').text
    except:
        Number_reviews = 0
    try:
        App_Name = driver.find_element_by_class_name('AHFaub').text
    except:
        App_Name = 'No Name'
    try:
        genre = driver.find_element_by_class_name('qQKdcc').text
    except:
        genre = 'Not Specified'
    try:
        Details= driver.find_elements_by_class_name('htlgb')
        detail_text = []
        for j in Details:
            detail_text.append(j.text)
    
        Details = []
        for j in range(len(detail_text)//2):
            Details.append(detail_text[2*j])
    except:
        Details = 'No Details'
    entry = {'App Name':App_Name, 'Details':Details, 'Genre':genre, 
             'Rating':rating, 'Number of Reviews': Number_reviews}
    
    entry = pd.Series(entry)
    app_data = app_data.append(entry, ignore_index = True)
    
    time.sleep(2)
    
app_data.to_csv('play_store_data.csv', index = False)

