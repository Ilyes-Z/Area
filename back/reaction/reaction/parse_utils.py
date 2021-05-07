import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib
import requests

def get_token(service_name, user_id, twitch=False):
    resp = requests.get('http://parse-server:1337/parse/Users/{}'.format(user_id),
        headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": "parse@master123!"})

    data = resp.json()
    if twitch:
        return data["auth_service"]["{}".format(service_name)]["access_token"], data["auth_service"]["{}".format(service_name)]["client_id"]
    return data["auth_service"]["{}".format(service_name)]["access_token"]


def get_reaction_data(couple_id):
    resp = requests.get('http://parse-server:1337/parse/classes/Area/{}'.format(couple_id),
        headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": "parse@master123!", "Content-Type": "application/json"})
    if resp.status_code != 200:
        raise ValueError("Bad request, area not found !")

    return resp.json()

def get_reaction_service(service_id):
    resp = requests.get('http://parse-server:1337/parse/classes/Service/{}'.format(service_id),
    headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": "parse@master123!", "Content-Type": "application/json"})

    if resp.status_code != 200:
        raise ValueError("Bad request, service reaction not found !")

    return resp.json()
