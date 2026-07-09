from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd
import numpy as np
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Creates access token for Spotify API
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """
    Returns information related to an artist by ARTIST NAME
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    # result = get(query_url, headers = headers)
    # json_result = json.loads(result.content)["artists"]["items"]
    # if len(json_result) == 0:
    #     print("No artist with this name exists...")
    #     return None
    # return json_result[0]
    while True:
        result = get(query_url, headers=headers)
        
        if result.status_code == 429:  # Rate limit exceeded
            retry_after = int(result.headers.get("Retry-After", 5))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue 

        if result.status_code != 200:
            print(f"Error fetching artist: {result.status_code}")
            return None
        
        try:
            json_result = json.loads(result.content)["artists"]["items"]
            if len(json_result) == 0:
                print("No artist with this name exists...")
                return None
            return json_result[0]
        
        except json.JSONDecodeError:
            print("Failed to decode JSON for song search.")
            return None

def search_for_artist_via_id(token, artist_id):
    """
    Returns information related to an artist by ARTIST ID
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    
    # result = get(query_url, headers = headers)
    # json_result = json.loads(result.content)["artists"]["items"]
    # if len(json_result) == 0:
    #     print("No artist with this name exists...")
    #     return None
    # return json_result[0]
    while True:
        result = get(url, headers=headers)
        
        if result.status_code == 429:  # Rate limit exceeded
            retry_after = int(result.headers.get("Retry-After", 5))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue 

        if result.status_code != 200:
            print(f"Error fetching artist: {result.status_code}")
            return None
        
        try:
            json_result = json.loads(result.content)
            if len(json_result) == 0:
                print(f"No artist with this id exists...{artist_id}")
                return None
            return json_result
        
        except json.JSONDecodeError:
            print("Failed to decode JSON for song search.")
            return None

def search_for_song(token, track_name, artist_name):
    """
    Returns info about a track found by SONG NAME and ARTIST NAME
    Main use is to retrieve track id
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=track:{track_name} artist:{artist_name}&type=track&limit=1"
    query_url = url + query
    # result = get(query_url, headers=headers)
    # print(result)
    # json_result = json.loads(result.content).get("tracks", {}).get("items", [])
    
    # if len(json_result) == 0:
    #     print("No track with this name and artist exists...")
    #     return None
    # return json_result[0]
    while True:
        result = get(query_url, headers=headers)
        
        if result.status_code == 429:  # Rate limit exceeded
            retry_after = int(result.headers.get("Retry-After", 5))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue 

        if result.status_code != 200:
            print(f"Error fetching song: {result.status_code}")
            return None
        
        try:
            json_result = json.loads(result.content).get("tracks", {}).get("items", [])
            if len(json_result) == 0:
                print("No track with this name and artist exists...")
                return None
            return json_result[0]
        
        except json.JSONDecodeError:
            print("Failed to decode JSON for song search.")
            return None

def get_audio_features(token, track_id):
    """
    Returns audio features of a given song by its TRACK ID
    """
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code != 200:
        print(f"Error fetching audio features: {result.status_code}")
        return None
    json_result = json.loads(result.content)
    return json_result


def get_audio_features_for_tracks(token, track_ids):
    """
    Returns audio features for multiple tracks by their TRACK IDs
    """
    url = "https://api.spotify.com/v1/audio-features"
    headers = get_auth_header(token)
    params = {"ids": ",".join(track_ids)}
    
    # result = get(url, headers=headers, params=params)
    # if result.status_code != 200:
    #     print(f"Error fetching audio features: {result.status_code}")
    #     return None
    # return json.loads(result.content).get("audio_features", [])

    while True:
        result = get(url, headers=headers, params=params)
        
        if result.status_code == 429:  # Rate limit exceeded
            retry_after = int(result.headers.get("Retry-After", 5))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue 

        if result.status_code != 200:
            print(f"Error fetching audio features: {result.status_code}")
            return None
        
        try:
            return json.loads(result.content.get("audio_features", []))
        
        except json.JSONDecodeError:
            print("Failed to decode JSON for audio features batch search.")
            return None    

def get_songs_by_artist(token, artist_id):
    """
    Returns list of top songs for an artist by their ARTIST ID 
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_genres_of_artist(token, artist_id):
    """
    Returns list of genres an artist is involved with by their ARTIST ID
    """
    genres = search_for_artist_via_id(token, artist_id)
    if genres is None:
        print(f"No genres found for {artist_id}")
        return None
    return genres["genres"]
    
def get_track_by_id(token, track_id):
    """
    Returns info of a song via its TRACK ID
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code != 200:
        print(f"Error fetching track: {result.status_code}")
        return None
    json_result = json.loads(result.content)
    return json_result
    




token = get_token()
last_refresh = time.time()

# df_tweets = pd.read_csv('mmtd\\mmtd.txt', sep='\t')
df_tweets = pd.read_csv('DataSets\\unique_temp_16000.csv')

"""
MAKE SURE TO CHANGE THE NEXT LINE IF YOURE READING FROM A TEMP FILE
if u dont then previous history is deleted as track id, genres, and
popularity aren't kept.
"""

#THIS ONE
# unique_tracks = df_tweets[['artist_name', 'track_title']]
unique_tracks = df_tweets

unique_tracks = unique_tracks.drop_duplicates()
print(f"Dimensions: {unique_tracks.shape}")

unique_tracks['track_id'] = pd.Series(dtype='object')
unique_tracks['popularity'] = np.nan
unique_tracks['artist_genres'] = pd.Series(dtype='object')
audio_features_columns = [
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]
for col in audio_features_columns:
    unique_tracks[col] = np.nan


"""""""""""""""""""""""""""""""""""""""""
GENRES FOR ROW ENTRIES < 6660 ARE WRONG
oopsies
"""""""""""""""""""""""""""""""""""""""""

# Retrieving track IDs using search_for_song
# if starting from one of the temp files, set the
# iloc index to two less than file name
# example: [15998:] when using unique_temp_16000.csv, remember to keep the colon
for index, row in unique_tracks.iloc[15998:].iterrows():
    if time.time() - last_refresh > 3300:
        token = get_token()
        last_refresh = time.time()
        print("TOKEN REFRESHED")
        time.sleep(3)
    
    if index % 1000 == 0:
        unique_tracks.to_csv(f"unique_temp_{index}.csv", index=True, header=True)

    song_info = search_for_song(token, row['track_title'], row['artist_name'])
    
    if song_info:
        unique_tracks.at[index, 'track_id'] = song_info['id']
        unique_tracks.at[index, 'popularity'] = song_info['popularity']
        
        artist_id = song_info['artists'][0]['id']
        genres = get_genres_of_artist(token, artist_id)
        unique_tracks.at[index, 'artist_genres'] = ', '.join(genres) if genres else np.nan
        
        time.sleep(0.2)
    print(f"Completed Search for song: {index}")
    print(f"Artist name: {unique_tracks.at[index, 'artist_name']}")
    print(f"Track ID: {unique_tracks.at[index, 'track_id']}")

unique_tracks = unique_tracks.dropna(subset=['track_id'])
unique_tracks.to_csv('unique_tracks_no_audio.csv', index=True, header=True)

# Retrieving audio features in batches for found track IDs
track_ids = unique_tracks['track_id'].tolist()
batch_size = 50
for i in range(0, len(track_ids), batch_size):
    batch = track_ids[i:i + batch_size]
    if time.time() - last_refresh > 3300:
        token = get_token()
        last_refresh = time.time()
        print("TOKEN REFRESHED")
        time.sleep(3)

    if i % 1000 == 0:
        unique_tracks.to_csv(f"unique_temp2_{index}.csv", index=True, header=True)
    
    audio_features = get_audio_features_for_tracks(token, batch)
    
    # Process and merge audio features back to the DataFrame
    for features in audio_features:
        if features:  
            track_id = features['id']
            for col in audio_features_columns:
                unique_tracks.loc[unique_tracks['track_id'] == track_id, col] = features[col]
    time.sleep(0.2)
    print(f"Completed audio features for batch: {i}")

print(unique_tracks.head())

unique_tracks.to_csv('unique_tracks_info.csv', index=True, header=True)