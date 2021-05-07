import http.client
import json
from django.http import HttpResponse
from middleware_area import utils
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib
import requests

class Services(APIView):
    def __get_user_services(self, request, resp):
        user = utils.get_user_from_headers(request.headers)

        if user is None:
            return Response("Unauthorized", status=401)
        auth = user.get('auth_service', {})

        services_name = []
        for key in auth.keys():
            services_name.append(key)

        services = []
        for service in resp:
            if service['name'] not in services_name:
                service["connected"] = False
                service["auth_required"] = auth.get(service["name"], {}).get("auth_required", True)
                services.append(service)
            else:
                service["connected"] = auth.get(service["name"], {})["connected"]
                service["auth_required"] = auth.get(service["name"], {}).get("auth_required", True)
                services.append(service)

        return Response({'results': services}, status=200)

    def get(self, request, *args, **kwargs):
        resp = requests.get('http://parse-server:1337/parse/classes/Service',
        headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": ""
        })
        auth = request.headers.get('Authorization', None)
        if auth is not None:
            return self.__get_user_services(request, resp.json()['results'])

        return Response(resp.json(), status=resp.status_code)

class Service(APIView):
    def delete(self, request, *args, **kwargs):
        name = kwargs.get('service_name', None)
        if name is None:
            return HttpResponse('Service not found', status=404)
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            return Response("Unauthorized", status=401)

        if user["auth_service"][name] is None:
            return Response(None, status=200)

        token = request.headers['Authorization'].split("Bearer ")[1]
        auth = user["auth_service"]
        auth[name] = {
            "connected": False,
            "auth_required": user["auth_service"][name]["auth_required"]
        }
        resp = requests.put("http://parse-server:1337/parse/users/" + user["objectId"],
        data=json.dumps({"auth_service": auth}),
        headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": "",
            "X-Parse-Session-Token": token,
            "Content-Type": "application/json"
        })

        return Response(resp.json(), status=resp.status_code)

    def get(self, request, *args, **kwargs):
        name = kwargs.get('service_name', None)
        if name is None:
            return HttpResponse('Service not found', status=404)

        connection = http.client.HTTPConnection('parse-server:1337')
        connection.connect()
        params = urllib.parse.urlencode(
        {
            "where": json.dumps({
                "name": {"$regex": "(?i){}".format(name)}
        })})
        connection.request('GET', '/parse/classes/Service?%s' % params, '', {
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": ""
        })

        result = json.loads(connection.getresponse().read())
        if len(result["results"]) == 0:
            return HttpResponse('Service not found', status=404)
        return Response(result["results"][0], status=200)