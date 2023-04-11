import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

client_id = os.environ.get('CLIENTID')
client_secret = os.environ.get('CLIENTSECRET')
playlist_uri = os.environ.get('PLAYLIST_URI')
playlist_id = os.environ.get('PLAYLIST_ID')
playlist_name = os.environ.get('PLAYLIST_NAME')
username = os.environ.get('USERNAME')
tracks = []

if not client_id:
    raise ValueError('SPOTIFY_CLIENT_ID environment variable not set')

if not client_secret:
    raise ValueError('CLIENTSECRET environment variable not set')


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://localhost:8080/callback",
                                               scope="playlist-modify"))


# Read the song names from the file
with open("playlist.txt", "r") as f:
    song_names = [line.strip() for line in f.readlines()]

playlist_tracks = sp.playlist_tracks(playlist_id)

for item in playlist_tracks['items']:
    tracks.append(item['track']['id'])

for song_name in song_names:
    results = sp.search(q=song_name, type="track", limit=1)

    if results["tracks"]["total"] <= 0:
        continue

    new_track_uri = results["tracks"]["items"][0]["uri"]
    new_track_id = results["tracks"]["items"][0]["id"]

    if new_track_id in tracks:
        print(f"Song already in playlist: {song_name}")
        continue

    if sp.playlist_add_items(playlist_uri, [new_track_uri], None):
        print(f"New song in playlist: {song_name}")
