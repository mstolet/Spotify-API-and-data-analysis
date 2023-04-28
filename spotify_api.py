import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Enter your Spotify API credentials
client_id = '301624a72c384c9a9a9601ec7c2a5266'
client_secret = 'b65eed47938e4d01acd8202d1d93d004'

# Create a Spotify client object
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the search query
search_query = 'pesadão'

# Search for playlists with the word "pesadão" in the name
results = sp.search(search_query, type='playlist', limit=3)

# Create a dictionary to store the number of listeners per country
listeners_per_country = {}

# Loop through each playlist and get the number of listeners per country for each track
for playlist in results['playlists']['items']:
    # Get the playlist ID
    playlist_id = playlist['id']

    # Get the tracks from the playlist
    tracks = sp.playlist_tracks(playlist_id)

    # Loop through each track and get the number of listeners per country
    for track in tracks['items']:
        # Get the track ID
        track_id = track['track']['id']

        # Get the audio features for the track
        audio_features = sp.audio_features(track_id)[0]

        # Get the country with the most listeners
        country = audio_features['analysis_url']

        # Add the country to the dictionary
        if country in listeners_per_country:
            listeners_per_country[country] += track['track']['popularity']
        else:
            listeners_per_country[country] = track['track']['popularity']

# Create a pandas dataframe from the dictionary
df = pd.DataFrame(list(listeners_per_country.items()), columns=['Country', 'Listeners'])

# Print the dataframe
print(df)
