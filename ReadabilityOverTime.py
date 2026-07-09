from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from readability import Readability
import nltk

def regular_linear_regression(x, y):
    X = np.c_[np.ones(x.shape[0]), x]
    try:
        # theta = (X^T X)^(-1) X^T y
        theta = np.linalg.inv(X.T @ X) @ X.T @ y
        return theta
    except np.linalg.LinAlgError:
        return np.nan

def predict_regular_linear_regression(x, theta):
    X = np.c_[np.ones(x.shape[0]), x] 
    return X @ theta

"""
Uncomment these next two lines just for the first ever run after you've used these commands in terminal:
   pip install py-readability-metrics
   python -m nltk.downloader punkt
"""
# nltk.download('punkt')
# nltk.download('punkt_tab')


# lyrics = pd.read_csv('DataSets\\tcc_ceds_music.csv')

# lyrics = lyrics.dropna(subset=['lyrics', 'release_date'])

# #Thought this would be an interest artist to make sure is included
# lyrics['artist_name'] = lyrics['artist_name'].replace('kanye west', 'kanye')

# lyrics.rename(columns={'track_name' : 'track_title'}, inplace=True)
# colsToKeep = ['artist_name', 'track_title', 'genre', 'lyrics', 'len', 'topic', 'release_date']
# lyrics = lyrics[colsToKeep]


# unique_songs = pd.read_csv('DataSets\\unique_tracks_info_noDupes.csv')
# unique_songs['artist_name'] = unique_songs['artist_name'].lower()
# unique_songs['track_title'] = unique_songs['track_title'].lower()
    
# df_merged = pd.merge(unique_songs, lyrics, on=['artist_name', 'track_title'])  

# df_merged.to_csv('merged_unique_lyrics.csv', header=True)  
         
unique_lyrics = pd.read_csv('DataSets\\merged_unique_lyrics.csv')
unique_lyrics['linsear_score'] = 0.0
unique_lyrics['read_pop_corr'] = 0.0
 
for index, row in unique_lyrics.iterrows():
    if unique_lyrics.loc[index, 'len'] >= 100:
        r = Readability(row['lyrics'])
        score = r.linsear_write().score
        unique_lyrics.loc[index, 'linsear_score'] = score


valid_scores = unique_lyrics[unique_lyrics['linsear_score'] != 0]

average_scores = valid_scores.groupby('release_date')['linsear_score'].mean().reset_index()
average_scores.columns = ['release_year', 'average_linsear_score']

twentyFirstCent = valid_scores[valid_scores['release_date'] >= 2000]
print(f"Correlation Between Popularity and Linsear Score Past 21st Century: {twentyFirstCent['popularity'].corr(twentyFirstCent['linsear_score'])}")


readability_lr = []
pop_lr = []

theta_read = regular_linear_regression(average_scores['release_year'].values, average_scores['average_linsear_score'].values)
theta_pop = regular_linear_regression(twentyFirstCent['linsear_score'].values, twentyFirstCent['popularity'].values)

for i in average_scores['release_year']:
    y_lr = predict_regular_linear_regression(np.array([i]), theta_read)
    readability_lr.append(y_lr[0])
for i in twentyFirstCent['linsear_score']:
    y_lr = predict_regular_linear_regression(np.array([i]), theta_pop)
    pop_lr.append(y_lr[0])

plt.figure(figsize=(10, 6))
plt.scatter(average_scores['release_year'], average_scores['average_linsear_score'])
plt.plot(average_scores['release_year'], readability_lr, label = 'Linear Regression Model', color='red')
print(f"Slope of Regression (Readability over Time): {theta_read[1]}")
# plt.scatter(valid_scores['release_date'], valid_scores['popularity'], alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Average Linsear Readability Score')
plt.title('Average Readability Score Over The Years')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(twentyFirstCent['linsear_score'], twentyFirstCent['popularity'])
plt.plot(twentyFirstCent['linsear_score'], pop_lr, label = 'Linar Regression Model', color='red')
print(f"Slope of Regression (Popularity over Readability): {theta_pop[1]}")
plt.xlabel('Linsear Score')
plt.ylabel('Popularity')
plt.title('Correlation Between Readability and Popularity (21st Century)')
plt.show()
        
    
