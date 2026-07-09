import requests
import pandas as pd
import time

# Function to query MusicBrainz API
def get_release_year(song_title, artist_name):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    query = f'?query=recording:"{song_title}" AND artist:"{artist_name}"&fmt=json'
    url = base_url + query
    
    try:
        # Make API request
        response = requests.get(url, headers={"User-Agent": "MyMusicApp/1.0"})
        response.raise_for_status()
        data = response.json()
        
        # Extract release year from the first recording found
        if data.get('recordings'):
            # Look for the release date in the first recording
            for release in data['recordings']:
                if release.get('first-release-date'):
                    return release['first-release-date'][:4]  # Extract the year
    except Exception as e:
        print(f"Error for song '{song_title}' by '{artist_name}': {e}")
    return None

# Read CSV
csv_file = 'unique_tracks_info_noDupes.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Add a release_year column
df['release_year'] = None

# Iterate over rows and query MusicBrainz
for index, row in df.iterrows():
    song_title = row['track_title']  # Replace with your column name
    artist_name = row['artist_name']  # Replace with your column name
    
    # Query API and update the DataFrame
    release_year = get_release_year(song_title, artist_name)
    print(release_year)
    df.at[index, 'release_year'] = release_year
    
    # Avoid hitting the API rate limit (1 request per second)
    time.sleep(.2)

# Save the updated DataFrame to a new CSV
df.to_csv('songs_with_release_year.csv', index=False)
print("Release year information saved to 'songs_with_release_year.csv'.")
