import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from middleware_area import utils
import requests

class Login(APIView):
    def __login_user_parse(self, email, username, password):
        params = {}
        if email is not None:
            params['email'] = email
        if username is not None:
            params['username'] = username
        params['password'] = password

        resp = requests.get("http://parse-server:1337/parse/login",
            params=params,
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Revocable-Session": "1"
            }
        )

        return Response(resp.json(), status=resp.status_code)

    def get(self, request, format=None):
        username = request.GET.get("username", None)
        email = request.GET.get("email", None)
        password = request.GET.get("password", None)
        if email is None and username is None:
            return Response("Bad request", status=400)
        if password is None:
            return Response("Bad request", status=400)
        return self.__login_user_parse(email, username, password)

class Register(APIView):
    def __register_user_parse(self, email, username, password):
        data = {
            "email": email,
            "username": username,
            "password": password
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

    def post(self, request, format=None):
        username = request.data.get("username", "")
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email is None or password is None:
            return Response("Bad request", status=400)
        return self.__register_user_parse(email, username, password)

class Delete(APIView):
    def delete(self, request, *args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if auth is None:
            return Response(None, status=401)
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            return Response("Unauthorized", status=401)
        token = auth.split("Bearer ")[1]
        resp = requests.delete("http://parse-server:1337/parse/users/" + user['objectId'],
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "X-Parse-Session-Token": token,
            }
        )
        return Response(resp.json(), status=resp.status_code)
