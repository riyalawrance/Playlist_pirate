import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI= os.getenv("REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="playlist-read-private"))

# playlist = sp.playlist_items("4YAtlXSKm45sJ35IgVzyR3")

# # print(playlist.keys())

# # for item in playlist["items"]:
# #     print(item["item"]["name"])

# # artist = sp.artist("06HL4z0CvFAxyc27GXpf02")  # Taylor Swift
# # print(artist["name"])

# album = sp.album_tracks("4yP0hdKOZPNshxUOjY0cZj")
# print(album["items"][0].keys())
# for item in album["tracks"]["items"]:
#     print(item["name"])

# track= sp.track("0WGZNNJzKRZJrRr7aasepC")
# print(track["name"],track["artists"][0]["name"])
# # try:
# #     playlist = sp.playlist("37i9dQZF1DXcBWIGoYBM5M")
# #     print(playlist["name"])
# # except Exception as e:
# #     print(e)

def get_playlist_tracks(playlist_id):
    tracks = []
    offset = 0

    while True:
        response = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=100
        )

        items = response["items"]

        if not items:
            break

        for item in items:
            track = item["item"]
            if track:
                tracks.append({
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"]
                })

        offset += 100

    return tracks

def get_album_tracks(album_id):
    tracks = []
    offset = 0

    while True:
        response = sp.album_tracks(
            album_id,
            offset=offset,
            limit=50
        )

        items = response.get("items", [])

        if len(items) == 0:
            break

        for item in items:
            tracks.append({
                "id": item["id"],
                "name": item["name"],
                "artist": item["artists"][0]["name"]
            })

        offset += 50

    return tracks

def get_tracks(track_id):
    tracks=[]
    item = sp.track(track_id)
    tracks.append({
        "id":track_id,
        "name": item["name"],
        "artist": item["artists"][0]["name"],
        "album": item["album"]["name"]
    })
    return tracks