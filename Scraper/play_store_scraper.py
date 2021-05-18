# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script file for scraping the app data on the Google Play Store.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from google_play_scraper import app
import time

url = 'https://play.google.com'

driver = webdriver.Chrome(executable_path = '/home/aryan/Documents/Git-Repos/App-Rating-Predictor/Scraper/chromedriver.exe')

driver.implicitly_wait(2)
driver.maximize_window()
driver.get(url +'/store/apps')
#letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
searches = ['Art & Design','Augmented reality','Auto & Vehicles','Beauty','Books & Reference','Business','Comics','Communication','Dating','Daydream','Education','Entertainment',
            'Events','Finance','Food & Drink','Health & Fitness','House & Home','Libraries & Demo','Lifestyle','Maps & Navigation','Medical','Music & Audio','News & Magazines',
            'Parenting','Personalization','Photography','Productivity','Shopping','Social','Sports','Tools','Travel & Local','Video Players & Editors','Wear OS by Google',
            'Weather','Action','Adventure','Arcade','Board','Card','Casino','Casual','Educational','Music','Puzzle','Racing','Role Playing','Simulation','Sports','Strategy',
            'Trivia','Word','Ages up to 5','Ages 6-8','Ages 9-12']

hrefs =[]
SCROLL_PAUSE_TIME = 1
for i in searches:
    driver.find_element_by_name('q').clear()
    time.sleep(0.5)
    driver.find_element_by_name('q').send_keys(i)
    time.sleep(1)
    driver.find_element_by_class_name('gbqfb').click()
    time.sleep(1.5)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        try:
            apps = driver.find_elements_by_class_name('poRVub')
            for j in range(len(apps)):
                hrefs.append(apps[j].get_attribute('href'))
        except:
            pass
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
            
        

app_data = pd.DataFrame()
print(len(np.unique(np.asarray(hrefs))))
print('test')
c = 0
links = np.unique(np.asarray(hrefs))
for i in links:
    print('{}/{}'.format(c+1, len(links)), end = '\r')
    c = c + 1
    try:
        id = i.split('=')[-1]
        entry = app(id, lang = 'en', country = 'in')
        entry = pd.Series(entry)
        app_data = app_data.append(entry, ignore_index = True)
    except:
        print("Could not retrieve data")    
    
app_data.to_csv('play_store_data.csv', index = False)

