# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:53:57 2020

@author: aryan
"""
import pandas as pd
import re

data = pd.read_csv('play_store_data.csv')

# Remove the word total from reviews
data['Number of Reviews'] = data['Number of Reviews'].apply(lambda x: int(x.split(' ')[0].replace(',','')))

# Get the genre from the genre column
data['Genre'] = data.apply(lambda x: x['Genre'].replace(x['Offered By'], ''), axis = 1)

data['Genre'] = data['Genre'].apply(lambda x: x.replace('ActionAction', 'Action'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('AdventureAction', 'Action'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('ArcadeAction', 'Action'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('CasualAction', 'Action'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('CasualCreativity', 'Casual'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('CasualEducation', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('EducationalBrain Games', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('EducationEducation', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('EducationalEducation', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('EducationalPretend Play', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('Educational', 'Education'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('EntertainmentMusic', 'Music'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('MusicMusic', 'Music'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('Role PlayingPretend Play', 'Role Playing'))
data['Genre'] = data['Genre'].apply(lambda x: x.replace('SimulationAction & Adventure', 'Simulation'))

#Get min and max prices from the In-app Purchases
data['In-app Purchases'] = data['In-app Purchases'].apply(lambda x: x.replace('Completely free', '$0 - $0 per item'))
data['Min Price'] = data['In-app Purchases'].apply(lambda x: x.split(' ')[0])
data['Max Price'] = data['In-app Purchases'].apply(lambda x:x.split(' ')[2])
data['Min Price'] = data['Min Price'].apply(lambda x: float(x[1:].replace(',','')))
data['Max Price'] = data['Max Price'].apply(lambda x: x[1:].replace(',',''))
def fix_max(row):
    if row['Max Price'] == 'tem':
        row['Max Price'] = row['Min Price']
    else:
        row['Max Price'] = float(row['Max Price'])
    return row
data = data.apply(fix_max, axis = 1)

# Convert Age rating to  Numeric form
data['Age'] = data['Minimum Age'].apply(lambda x: x.split(' ')[2])
data['Age'] = data['Age'].apply(lambda x: int(x.split('+')[0]))

# Convert Date to day, month, year features
data['Last Update'] = data['Last Update'].apply(lambda x: re.split(',| ', x))
data['Month'] = data['Last Update'].apply(lambda x: x[0])
month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 
              'June':6, 'July':7, 'August':8, 'September':9, 'October':10,
              'November':11, 'December':12}
data['Month'] = data['Month'].apply(lambda x: month_dict[x])
data['Day'] = data['Last Update'].apply(lambda x: int(x[1]))
data['Year'] = data['Last Update'].apply(lambda x: int(x[3]))

# Get minimum number of downloads from the number of installations column
data['Min Downloads'] = data['Number of Installations'].apply(lambda x: int(x[:-1].replace(',','')))

# Convert Size of the app to numeric feature
data['Size'] = data['Size'].apply(lambda x: -1 if x=='Varies with device' else float(x[:-1].replace(',','')))

# Convert Minimum Android version to Numeric
def fix_android(text):
    if text == 'Any version':
        return '0'
    elif text == 'Varies with device':
        return '-1'
    else:
        return text.split(' ')[0]
data['Minimum Android Version'] = data['Required Android Version'].apply(fix_android)

# Handle the Version feature
def fix_version(text):
    if text == 'Varies with device':
        return -1
    elif text == 'V106':
        return 1
    elif text == 'emarti_11.9.4':
        return 1
    elif text == 'version 1.5.2.0 b01':
        return 1
    elif text == 'version 2.21':
        return 2
    elif text == 'v1.5':
        return 1.5
    else:
        return int(text.split('.')[0])
data['Version'] = data['Version'].apply(fix_version)

# Getting an Interactive element score from the text data
element_dict = {'No Interactive Elements': 0, 'Users Interact':1, 'Digital Purchases':2,
                ' Digital Purchases':2, 'In-App Purchases':3, ' In-App Purchases':3, 
                'In-Game Purchases':3, ' In-Game Purchases':3, 'Shares Location':4, 
                ' Shares Location':4, 'Unrestricted Internet':5, ' Unrestricted Internet':5,
                'Shares Info':4, ' Shares Info':4}

def element_score(text):
    text_list = text.split(',')
    sum = 0
    for i in text_list:
        sum = sum + element_dict[i]
    return sum

data['Interactive Element Score'] = data['Interactive Elements'].apply(element_score)

# Uploading the Cleaned data
data.to_csv('Cleaned_data.csv', index = False)