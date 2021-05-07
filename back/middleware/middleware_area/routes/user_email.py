import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from base64 import b64encode
import os

class UserEmail(APIView):
    def post(self, request, format=None):
        email = request.data.get('email', None)
        if email is None:
            return Response("Malformated body", status=400)
        resp = requests.post("http://parse-server:1337/parse/requestPasswordReset",
            data=json.dumps({
                "email": email
            }),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "Content-Type": "application/json"
            }
        )
        return Response(resp.json(), status=resp.status_code)