import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up the authentication credentials

client_id = os.environ.get('CLIENTID')
client_secret = os.environ.get('CLIENTSECRET')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://localhost:8080/callback",
                                               scope="user-top-read"))

ranges = ['long_term']

for sp_range in ranges:
    print("range:", sp_range)

    results = sp.current_user_top_artists(time_range=sp_range, limit=100)

    for i, item in enumerate(results['items']):
        print(i, item['name'])
    print()


# Get the top 100 most played tracks
results = sp.current_user_top_tracks(limit=100, time_range="long_term")
# Print the name and artist of each track
for i, item in enumerate(results['items']):
    print(f"{i+1}. {item['name']} - {item['artists'][0]['name']}")
