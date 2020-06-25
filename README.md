# App-Rating-Predictor (Project in-progress)

## Introduction
This Project uses data from the apps on the Google Play Store to predict the overall rating a particular app will get from its users. There are a variety of features which will be used by the model. There are approximately 850 training apps and 150 testing apps. Model Accuracy will be uploaded once the Model Building stage is complete.

## Web Scraper using Selenium
For getting the data from the Google Play Store this project uses a Selenium based Web Scraper Python script. The script first gets the search results for each letter of the English Alphabet and stores the URLs for each app in a list. After this it iterates through all the unique URLs and grabs the data related to every app.

The data columns which it grabs for each app are : Name, Genre, Last Update, Age Requirement, Android Version Requirement, Number of installations, Current Version, Size, Interactive elements, Company Owned by, The Name of the Developer, Number of Reviews and the Overall Rating of the app. 

Link for the Python Web Scraper - [Web Scraper](Scraper/play_store_scraper.py) 
