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

class ThirdPartyAuth(APIView):
    def post(self, request, *args, **kwargs) :
        resp = requests.post(PARSE_ADDRESS + "/parse/users",
            data=request.data,
            headers={
                "X-Parse-Application-Id": PARSE_APP,
                "X-Parse-REST-API-Key": "",
                "X-Parse-Revocable-Session": "1",
                "Content-Type": "application/json"
            }
        )

        return Response(resp.data, resp.status_code, {"Content-Type": "application/json"})
