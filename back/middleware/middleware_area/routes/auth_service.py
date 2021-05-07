import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from base64 import b64encode
import os

PARSE_ADDRESS   ="http://parse-server:1337"
PARSE_APP       =""

class Spotify(APIView):
    def __user_spotify(self, session, token):
        resp = requests.get("https://api.spotify.com/v1/me",
            headers={
                "Authorization": "Bearer {}".format(token["access_token"])
            }
        )

        if resp.status_code != 200:
            return Response(resp.json(), status=resp.status_code)

        user = resp.json()
        data = {
            "authData": {
                "soptify": {
                    "id": user["id"],
                    "access_token": token["access_token"]
                }
            }
        }
        resp = requests.post("http://parse-server:1337/parse/users",
            data=json.dumps(data),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Revocable-Session": "1",
                "Content-Type": "application/json"
            }
        )
        return Response(resp.json(), status=resp.status_code)

    def __save_user_token(self, user, session, token):
        if user is None:
            return self.__user_spotify(session, token)
        auth = user.get("auth_service", {})
        auth["Spotify"] = {
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)

        return Response(None, status=200)

    def __get_spotify_data(self, code):
        redirect = ("https://api.area-revenge.ninja/service/spotify/callback", "http://localhost:8080/service/spotify/callback")[os.environ.get("AREA_HOST", "") == "localhost"]
        print("Redirect: ", redirect)
        resp = requests.post('https://accounts.spotify.com/api/token', data={
            'grant_type': "authorization_code",
            'code': code,
            'redirect_uri': redirect
        }, headers={
            "Authorization": ""
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        error = request.GET.get("error", None)
        if error is not None:
            return Response(None, status=400)
        session = request.GET.get("state", None)
        user = None
        if session is not None:
            user = self.__get_user(session)
            if user is None:
                return HttpResponse("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_spotify_data(code)
        if token is None:
            return Response(None, status=400)

        return self.__save_user_token(user=user, session=session, token=token)

class GithubOAuth(APIView):
    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth["Github"] = {
            "access_token": token['access_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)

        return Response(None, status=200)

    def __get_github_data(self, code):
        resp = requests.post('https://github.com/login/oauth/access_token',
        params={
            "client_id": "",
            "client_secret": "",
            "code": code,
            "redirect_uri": "https://api.area-revenge.ninja/service/github/callback"
        }
        , headers={
            "Accept": "application/json"
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })
        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        session = request.GET.get("state", None)
        if session is None:
            return HttpResponse("Bad request, it miss session token", status=400)

        user = self.__get_user(session)
        if user is None:
            return HttpResponse("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_github_data(code)
        if token is None:
            return Response(None, status=400)

        return self.__save_user_token(user=user, session=session, token=token)

class AzureOAuth(APIView):

    SERVICE_NAME = "Azure"

    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth[self.SERVICE_NAME] = {
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token'],
            "id_token": token['id_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put(PARSE_ADDRESS + "/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": PARSE_APP,
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)

        return Response(None, status=200)

    def __get_azure_data(self, code):
        resp = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data={
            "client_id": "",
            "client_secret": "",
            "grant_type" : "authorization_code",
            "code": code,
            "redirect_uri": ("https://api.area-revenge.ninja/service/azure/callback", "http://localhost:8080/service/azure/callback")[os.getenv("AREA_HOST", "") == "localhost"]
        }
        , headers={
            "Accept": "application/json"
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get(PARSE_ADDRESS + "/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })
        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        session = request.GET.get("state", None)
        if session is None:
            return HttpResponse("Bad request, missing session token", status=400)

        user = self.__get_user(session)
        if user is None:
            return HttpResponse("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_azure_data(code)
        if token is None:
            return Response(None, status=400)

        return self.__save_user_token(user=user, session=session, token=token)

class DiscordOAuth(APIView):
    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth["Discord"] = {
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            print("save discord user fail", resp.json())
            return Response(resp.text, status=resp.status_code)
        return Response(None, status=200)

    def __get_discord_data(self, code):
        resp = requests.post('https://discord.com/api/v8/oauth2/token',
        data={"client_id": "",
            "client_secret": "",
            'grant_type': 'authorization_code',
            "code": code,
            "redirect_uri": ("https://api.area-revenge.ninja/service/discord/callback", "http://localhost:8080/service/discord/callback")[os.environ.get("AREA_HOST", "") == "localhost"],
            "scope": "connections guilds email identify"
        }
        , headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        if resp.status_code != 200:
            print("get discord data fail", resp.json())
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })

        if resp.status_code != 200:
            print("get user discord fail", resp.json())
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        session = request.GET.get("state", None)
        if session is None:
            return HttpResponse("Bad request, it miss session token", status=400)
        user = self.__get_user(session)
        if user is None:
            return HttpResponse("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_discord_data(code)
        if token is None:
            print("get discord token fail")
            return Response(None, status=400)
        return self.__save_user_token(user=user, session=session, token=token)

class RedditOAuth(APIView): # Not finish
    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth["Reddit"] = {
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)
        return Response(None, status=200)

    def __get_reddit_data(self, code):
        userAndPass = b64encode(b"nQb5YFaOPgdNeg:G1sunuQq-Rx71e2gAUDm8VSgDwFjZg").decode("ascii")
        resp = requests.post('https://www.reddit.com/api/v1/access_token',
        params={
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://api.area-revenge.ninja/service/reddit/callback"
        }, headers={'Authorization' : 'Basic %s' %  userAndPass})

        print('Url: ', resp.url)
        if resp.status_code != 200:
            print("Resp Code: ", resp.status_code)
            print("Resp: ", resp.json())
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        error = request.GET.get("error", None)
        if error is not None:
            return Response("We get error when callback", status=400)
        session = request.GET.get("state", None)
        if session is None:
            return Response("Bad request, it miss session token", status=400)

        user = self.__get_user(session)
        if user is None:
            return Response("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_reddit_data(code)
        if token is None:
            return Response("Token not found", status=400)

        return self.__save_user_token(user=user, session=session, token=token)

class TwitchOAuth(APIView):
    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth["Twitch"] = {
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token'],
            "client_id": "",
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)

        return Response(None, status=200)

    def __get_twitch_data(self, code):
        resp = requests.post('https://id.twitch.tv/oauth2/token',
        params={
            "client_id": "",
            "client_secret": "",
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": ("https://api.area-revenge.ninja/service/twitch/callback", "http://localhost:8080/service/twitch/callback")[os.environ.get("AREA_HOST", "") == "localhost"]
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        session = request.GET.get("state", None)
        if session is None:
            return HttpResponse("Bad request, it miss session token", status=400)

        user = self.__get_user(session)
        if user is None:
            return HttpResponse("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_twitch_data(code)
        if token is None:
            return Response(None, status=400)

        return self.__save_user_token(user=user, session=session, token=token)

class StackOverflowOAuth(APIView):
    def __save_user_token(self, user, session, token):
        auth = user.get("auth_service", {})
        auth["Stackoverflow"] = {
            "access_token": token['access_token'],
            "auth_required": True,
            "connected": True
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
            data=json.dumps({"auth_service": auth}),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": session,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            return Response(resp.text, status=resp.status_code)
        return Response(None, status=200)

    def __get_stackoverflow_data(self, code):
        resp = requests.post('https://stackoverflow.com/oauth/access_token/json',
        params={
            "client_id": "",
            "client_secret": "",
            "code": code,
            "redirect_uri": "https://api.area-revenge.ninja/service/stackoverflow/callback"
        }, headers={'Content-Type' : 'application/x-www-form-urlencoded'})

        print("Resp Code: {} Status code: {}".format(resp.json(), resp.status_code))
        if resp.status_code != 200:
            print("Resp Code: {} Status code: {}".format(resp.json(), resp.status_code))
            return None
        return resp.json()

    def __get_user(self, session):
        resp = requests.get("http://parse-server:1337/parse/users/me", headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": session
        })

        if resp.status_code != 200:
            return None
        return resp.json()

    def get(self, request, *args, **kwargs):
        error = request.GET.get("error", None)
        if error is not None:
            return Response("We get error when callback", status=400)
        session = request.GET.get("state", None)
        if session is None:
            return Response("Bad request, it miss session token", status=400)

        user = self.__get_user(session)
        if user is None:
            return Response("User not found", status=404)
        code = request.GET.get("code")
        token = self.__get_stackoverflow_data(code)
        if token is None:
            return Response("Token not found", status=400)

        return self.__save_user_token(user=user, session=session, token=token)