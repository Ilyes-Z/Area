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

URL_SEARCH_USER_ID = "https://api.twitch.tv/helix/users?login={}"

URL_FOLLOW_USER = "https://api.twitch.tv/helix/users/follows"

CLIENT_ID_FOR_TEST = "su5beoyoyg7z8ihwfcx4bpelsr0043"

def twitch_parser(request, area_data, reaction_index):
    if area_data["reaction"][reaction_index]["id"] == "twitch-follow-user":
        follow_user(request, area_data, reaction_index)


def get_user_id(following_name, username, access_token, client_id):

    resp = requests.get(URL_SEARCH_USER_ID.format(following_name),
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'Client-Id': client_id
    })

    if resp.status_code not in [200, 201]:
        raise ValueError('Error when get the id of the user {}. Error: {}, Code: {}'.format(following_name, resp.text, resp.status_code))
    data = json.loads(resp.text)
    following_id = data["data"][0]["id"]

    resp = requests.get(URL_SEARCH_USER_ID.format(username),
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'Client-Id': client_id
    })

    data = json.loads(resp.text)
    user_id = data["data"][0]["id"]

    return user_id, following_id


def follow_user(request, area_data, reaction_index):
    access_token, client_id = get_token("Twitch", area_data["user_id"], twitch=True)

    username = ""
    user_to_follow = ""
    params = area_data["reaction"][reaction_index]["parameters"]

    for param in params:
        if 'user-to-follow' in param:
            user_to_follow = param['user-to-follow']
        elif 'your-username' in param:
            username = param['your-username']

    user_id, following_id = get_user_id(user_to_follow, username, access_token, client_id)

    resp = requests.post(URL_FOLLOW_USER,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'Client-Id': client_id,
        'Content-Type': 'application/json'
    },json={
        'to_id': following_id,
        'from_id': user_id
    })

    if resp.status_code not in [204]:
        raise ValueError('Error when follow the user {}. Error: {}, Code: {}'.format(user_to_follow, resp.text, resp.status_code))
