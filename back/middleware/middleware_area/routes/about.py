import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import time

class About(APIView):
    def get(self, request, format=None):
        data = {
            "client": {
                "host": request.META.get('HTTP_X_REAL_IP', "localhost")
            },
            "server": {
                "current_time": int(round(time.time() * 1000)),
                "services": []
            }
        }

        resp = requests.get('http://parse-server:1337/parse/classes/Service',
        headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": ""
        })
        if resp.status_code != 200:
            return Response(data, status=200)
        services = resp.json()["results"]
        for service in services:
            toAdd = {
                "name": service["name"],
                "actions": [],
                "reactions": []
            }
            for trigger in service["triggers"]:
                action = {
                    "name": trigger['name'],
                    "description": trigger.get("desc", "")
                }
                toAdd["actions"].append(action)
            for reaction in service["reactions"]:
                action = {
                    "name": reaction['name'],
                    "description": reaction.get("desc", "")
                }
                toAdd["reactions"].append(action)
            data['server']['services'].append(toAdd)
        return Response(data, status=200)