from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data, get_reaction_service, get_token
from rest_framework.decorators import api_view, renderer_classes
from difflib import SequenceMatcher
import json


ADD_ITEM_TO_PLAYLIST = "https://api.spotify.com/v1/playlists/{}/tracks"

SEARCH_URL = "https://api.spotify.com/v1/search?query={}&type=track&limit=50&offset=0&market=from_token"

PLAYLIST_ID_FOR_TEST = "36GKTg4NhwchWaZJH7S6hr"

CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/{}/playlists"

GET_USER_URL = "https://api.spotify.com/v1/me"

LIKE_SONG = "https://api.spotify.com/v1/me/tracks?ids={}"

SEARCH_ARTISTE = "https://api.spotify.com/v1/search?q={}&type=artist&limit=10&offset=5&market=from_token"

GET_ARTIST_URL = "https://api.spotify.com/v1/me/following?type=artist&ids={}"

def get_songs_ids(song_list, access_token):
    resp = None
    song_id = []

    for song in song_list:
        resp = requests.get(SEARCH_URL.format(str(song).replace(" ", "+")), headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if resp.status_code != 200:
            raise ValueError('Error when charging song id of : {}. Error : {} , code = {}'.format(
                song, resp.text, resp.status_code))
        data = json.loads(resp.text)

        best = 0
        uri = ""
        for item in data["tracks"]["items"]:
            if item["popularity"] > best:
                best = item["popularity"]
                uri = item["uri"]

        song_id.append(uri)

    return song_id


def get_artist_ids(artist, access_token):
    resp = None
    artist_id = 0

    resp = requests.get(SEARCH_URL.format(artist), headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    if resp.status_code != 200:
        raise ValueError('Error when charging artist id of : {}. Error : {} , code = {}'.format(artist, resp.text, resp.status_code))
    data = json.loads(resp.text)
    best = 0
    for item in data["tracks"]["items"]:
        if item["popularity"] > best:
            best = item["popularity"]
            artist_id = item["artists"][0]["id"]
    return artist_id


def spotify_parser(request, area_data, reaction_index):
    print("Reaction for Spotify service !")
    if area_data["reaction"][reaction_index]["id"] == "spotify-add-song":
        add_songs_to_playlists(request, area_data, reaction_index)
    elif area_data["reaction"][reaction_index]["id"] == "spotify-create-playlist":
        create_playlist(request, area_data, reaction_index)
    elif area_data["reaction"][reaction_index]["id"] == "spotify-like-song":
        like_song(request, area_data, reaction_index)
    elif area_data["reaction"][reaction_index]["id"] == "spotify-follow-artist":
        follow_artist(request, area_data, reaction_index)


def get_username(access_token):
    resp = requests.get(GET_USER_URL,
    headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    })

    if resp.status_code not in [200, 201]:
        raise ValueError('Error when get user data for spotify. Error: {}, Code: {}'.format(
            resp.text, resp.status_code))

    data = json.loads(resp.text)

    return data["display_name"]


def create_playlist(request, area_data, reaction_index):
    access_token = get_token("Spotify", area_data["user_id"])
    username = get_username(access_token)

    resp = requests.post(CREATE_PLAYLIST_URL.format(username),
    headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"

    }, json={
        'name': area_data["reaction"][reaction_index]["parameters"][0]["playlist-name"]
    }
    )

    if resp.status_code not in [200, 201]:
        raise ValueError('Error when create the playlist {}. Error: {}, Code: {}'.format(
            area_data["reaction"][reaction_index]["parameters"][0]["playlist-name"], resp.text, resp.status_code))


def add_songs_to_playlists(request, area_data, reaction_index):
    print("Spotify add song to playlist for user: ", area_data["user_id"])
    access_token = get_token("Spotify", area_data["user_id"])
    song_id = get_songs_ids(area_data["reaction"][reaction_index]["parameters"][0]["song-list"], access_token)
    playlists_new = []

    if request["data"]["data"]["playlists"]:
        playlists_new = request["data"]["data"]["playlists"]
    else:
        params = area_data["reaction"][reaction_index]["parameters"]
        for param in params:
            if 'playlist' in param:
                playlists_new.append(param['playlist'])

    for playlist in playlists_new:
        playlist_data_for_request = ""
        for song in song_id:
            playlist_data_for_request += "{},".format(song)

        resp = requests.post(ADD_ITEM_TO_PLAYLIST.format(playlist),
        params={"uris": playlist_data_for_request },
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if resp.status_code not in [200, 201]:
            raise ValueError("Error when add song on the spotify playlist. Error : {} , Code = {}".format(
                resp.text, resp.status_code))
    print("Add song to playlist was accepted !")


def like_song(request, area_data, reaction_index):
    access_token = get_token("Spotify", area_data["user_id"])
    song_name = [area_data["reaction"][reaction_index]
        ["parameters"][0]["song-name"]]
    ids = get_songs_ids(song_name, access_token)

    resp = requests.put(LIKE_SONG.format(ids[0].replace('spotify:track:', '')),
    headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    )
    if resp.status_code not in [200, 201]:
        raise ValueError('Error when like the song: {}. Error: {}, Code: {}'.format(
            area_data["reaction"][reaction_index]["parameters"][0]["song-name"], resp.text, resp.status_code))

def follow_artist(request, area_data, reaction_index):
    access_token = get_token("Spotify", area_data["user_id"])
    artist_name = area_data["reaction"][reaction_index]["parameters"][0]["artist-name"]
    print(artist_name)
    id = get_artist_ids(artist_name, access_token)
    print(id)
    resp = requests.put(GET_ARTIST_URL.format(id),
    headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    )
    if resp.status_code not in [200, 201, 204]:
        raise ValueError('Error when follow artist : {}. Error: {}, Code: {}'.format(
            artist_name, resp.text, resp.status_code))
