NOWPLAYING-RS DATASET
************************************

The nowplaying-rs dataset features context- and content features of listening events. It contains 11.6 million music listening events of 139K users and 346K tracks collected from Twitter. The dataset comes with a rich set of item content features and user context features, as well as timestamps of the listening events. Moreover, some of the user context features imply the cultural origin of the users, and some others - like hashtags - give clues to the emotional state of a user underlying a listening event.

The dataset contains three files:
* user_track_hashtag_timestamp.csv contains basic information about each listening event. For each listening event, we provide an id, the user_id, track_id, hashtag, created_at
* context_content_features.csv: contains all context and content features. For each listening event, we provide the id of the event, user_id, track_id, artist_id, content features regarding the track mentioned in the event (instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, mode, key) and context features regarding the listening event (coordinates (as geoJSON), place (as geoJSON), geo (as geoJSON), tweet_language, created_at, user_lang, time_zone contained in the tweet). 
* sentiment_values.csv contains sentiment information for hashtags. It contains the hashtag itself and the sentiment values gathered via four different sentiment
dictionaries: AFINN, Opinion Lexicon, Sentistrength Lexicon and vader. For each of these dictionaries we list the minimum, maximum, sum and average of all
sentiments of the tokens of the hashtag (if available, else we list empty values). However, as most hashtags only consist of a single token, these
values are equal in most cases. Please note that the lexica are rather diverse and therefore, are able to resolve very different terms against a score. Hence,
the resulting csv is rather sparse. The file contains the following comma-separated values: <hashtag, vader_min, vader_max, vader_sum,vader_avg,  afinn_min, afinn_max,
afinn_sum, afinn_avg, ol_min, ol_max, ol_sum, ol_avg, ss_min, ss_max, ss_sum, ss_avg >, where we abbreviate all scores gathered over the Opinion Lexicon with the
prefix 'ol'. Similarly, 'ss' stands for SentiStrength.


Please note that user_track_hashtag_timestamp.csv and context_content_features.csv partly provide the same features. We deliberately chose to do so to be able to provide useable files that do not have to be matched and joined with each other to perform e.g., simple recommendation tasks.

Please find the training and test-splits for the dataset on https://dbis-nowplaying.uibk.ac.at. Also, Asmita provides prototypical implementations of a context-aware recommender system based on the dataset at https://github.com/asmitapoddar/nowplaying-RS-Music-Reco-FM.


If you make use of this dataset, please cite the following paper where we describe and experiment with the dataset:

@inproceedings{smc18,
title = {#nowplaying-RS: A New Benchmark Dataset for Building Context-Aware Music Recommender Systems},
author = {Asmita Poddar and Eva Zangerle and Yi-Hsuan Yang},
url = {http://mac.citi.sinica.edu.tw/~yang/pub/poddar18smc.pdf},
year = {2018},
date = {2018-07-04},
booktitle = {Proceedings of the 15th Sound & Music Computing Conference},
address = {Limassol, Cyprus},
note = {code at https://github.com/asmitapoddar/nowplaying-RS-Music-Reco-FM},
tppubtype = {inproceedings}
}


contact: 
Asmita Poddar
Eva Zangerle
Yi-Hsuan Yang
