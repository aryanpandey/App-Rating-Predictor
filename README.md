# App-Rating-Predictor (Project in-progress)

## Introduction
This Project uses data from the apps on the Google Play Store to predict the overall rating a particular app will get from its users. There are a variety of features which will be used by the model. There are approximately 850 training apps and 150 testing apps. The Ensemble of XGBoost, LightGBM and Catboost with weights as shown in the code gives an error of 6.4-6.8% which is the least possible from the models that were trained on.

## Web Scraper using Selenium
For getting the data from the Google Play Store this project uses a Selenium based Web Scraper Python script. The script first gets the search results for each letter of the English Alphabet and stores the URLs for each app in a list. After this it iterates through all the unique URLs and grabs the data related to every app.

The data columns which it grabs for each app are : Name, Genre, Last Update, Age Requirement, Android Version Requirement, Number of installations, Current Version, Size, Interactive elements, Company Owned by, The Name of the Developer, Number of Reviews and the Overall Rating of the app. 
The links for the script for the scraper and the scraped dataset can be found below:

Link for the Python Web Scraper - [Web Scraper](Scraper/play_store_scraper.py) 

Link for the dataset obtained after Web Scraping - [Data from Web Scraper](Data-Cleaning/play_store_data.csv)

## Cleaning the Data
Many of the columns in the data which has been scraped is not in the ideal form for performing some Exploratory Data Analysis. For example, the In-app Purchases feature has textual data like '$5 - $25 per item'. This form of data cannot be understood by a machine and we need to get it to a format where it will understand what is going on. For this purpose, Data Cleaning is done. The script to clean the data for this dataset and the cleaned dataset can be found in the link below:

Link for the Data Cleaner in Python - [Data Cleaner in Python](Data-Cleaning/cleaner.py)

Link to the Cleaned Dataset - [Cleaned Data](Cleaned_data.csv)

