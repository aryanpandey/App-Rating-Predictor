# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:53:57 2020

@author: aryan
"""
import pandas as pd
import re

data = pd.read_csv("play_store_data.csv")

# Drop duplicates according to Title
# Drop headerimage, descriptionHTML, Comments column as there is nothing there
# Check for rows which supports ads but don't support it, if exists make a new column
# Min android version
# Min Age rating
# Country sold in from currency
# BERT embeddings/word2vec followed by PCA/TSNE on the description
# Target Encode/Label Encode developer
# Clean Free column
# Check for genre similarity and clean. Label/Target encode. Contrast with GenreID
# Convert histogram to star wise rating columns
# Convert price to int
# Bins for installs
# Any discount from before?
# Num Ratings use to get total points (num Ratings times average)
# Word to vec/BERT on recent changes?
# Time for sale to end
# Number of reviews
# True Rating (Target variable, check if Upsampling might be needed)
# Size remove the M
# Summary also word2vec/BERT. What else can we do in NLP?
# Updated column inspect and fix/remove
