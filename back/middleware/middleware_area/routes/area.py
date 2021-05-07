import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from middleware_area import utils
import urllib
import requests

class HandleArea(APIView):
    def __send_area_creation(self, body):
        resp = requests.post('http://parse-server:1337/parse/classes/Area',
            data=json.dumps({
                'services': body['services'],
                'user_id': body['user_id'],
                'trigger': body['trigger'],
                'reaction': body['reaction']
            }), headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "Content-Type": "application/json"
            }
        )

        if resp.status_code != 201:
            return Response(resp.json(), status=resp.status_code)

        return Response({
            "objectId": resp.json()["objectId"],
            "created_at": resp.json()["createdAt"]
        }, status=202)

    def __get_parameters(self, services, trigger, reaction):
        resTri = requests.get('http://parse-server:1337/parse/classes/Service/' + services.get("trigger", ''),
            headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": ""})
        if resTri.status_code != 200:
            raise ValueError("Bad request, service trigger not found !")

        resRea = requests.get('http://parse-server:1337/parse/classes/Service/' + services.get("reaction", ''),
            headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": ""})
        if resRea.status_code != 200:
            raise ValueError("Bad request, service reaction not found !")

        try:
            triggerFilter = list(filter(lambda x: x["id"] == trigger, resTri.json().get("triggers", [])))
            if len(triggerFilter) == 0:
                raise ValueError("Bad request, trigger not found !")
        except:
            raise ValueError("Bad request, trigger doesn't exist !")

        try:
            reactionFilter = list(filter(lambda x: x["id"] == reaction, resRea.json().get("reactions", [])))
            if len(reactionFilter) == 0:
                raise ValueError("Bad request, reaction not found !")
        except:
            raise ValueError("Bad request, reaction doesn't exist !")

        return {"services": {"trigger": services['trigger'], "reaction": services['reaction']}, "trigger": triggerFilter[0]["parameters"], "reaction": reactionFilter[0]["parameters"]}


    def __fill_body_request(self, user, trigger, reaction, parameters):
        body = {}
        body['user_id']= user['objectId']
        body['services'] = parameters['services']
        body['reaction'] = []
        try:
            to_save = {}
            to_save["id"] = trigger["id"]
            to_save["parameters"] = []
            for param in parameters['trigger']:
                data = trigger.get(param["name"])
                to_save["name"] = param["name"]
                to_save["parameters"].append({
                    "type": param["type"],
                    param["id"]: data
                })
            body["trigger"] = to_save
        except:
            raise ValueError("Body malformated")

        try:
            to_save = {}
            to_save["parameters"] = []
            to_save["id"] = reaction["id"]
            for param in parameters['reaction']:
                data = reaction.get(param["name"])
                to_save["parameters"].append({
                    "type": param["type"],
                    param["id"]: data
                })
            body["reaction"].append(to_save)
        except:
            raise ValueError("Body malformated")
        return body

    def post(self, request, format=None):
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            return Response("Unauthorized", status=401)
        services = request.data.get('services', None)
        trigger = request.data.get('trigger', None)
        reaction = request.data.get('reaction', None)
        if services is None or trigger is None or reaction is None:
            return Response("Body mal formated", status=400)

        try:
            parameters = self.__get_parameters(services, trigger.get('id'), reaction.get('id'))
        except ValueError as err:
            return Response(err, status=400)

        body = None
        try:
            body = self.__fill_body_request(user, trigger, reaction, parameters)
        except ValueError as err:
            return Response(err, status=400)

        return self.__send_area_creation(body)

    def __get_list_area(self, user_id):
        payload = {'where': json.dumps({"user_id": user_id})}
        resp = requests.get('http://parse-server:1337/parse/classes/Area',
            params=payload,
            headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": ""})
        if resp.status_code != 200:
            return None

        return resp.json()

    def get(self, request, format=None):
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            return Response("Unauthorized", status=401)
        areas = self.__get_list_area(user['objectId'])
        if areas is None:
            return Response("Data not found", status=404)
        to_return = []
        for area in areas['results']:
            reactions = []
            for reac in area['reaction']:
                reactions.append(reac['id'])
            to_return.append({"objectId": area['objectId'], "is_actif": area['is_actif'], "trigger": area['trigger']['id'], "reactions": reactions})
        return Response(to_return, status=200)



class AreaInformation(APIView):
    def __active_desactive_area(self, area_id, is_actif):
        data = {
            "is_actif": is_actif,
        }
        resp = requests.put("http://parse-server:1337/parse/classes/Area/" + area_id,
            data=json.dumps(data),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "Content-Type": "application/json"
            }
        )
        return Response(resp.json(), status=resp.status_code)

    def __check_user_area(self, area_id, user_id):
        resp = requests.get('http://parse-server:1337/parse/classes/Area/' + area_id,
            headers={"X-Parse-Application-Id": "","X-Parse-REST-API-Key": ""})
        if resp.status_code != 200:
            return None

        if resp.json()['user_id'] != user_id:
            return None
        return resp.json()

    def __update_area(self, area, area_id):
        resp = requests.put("http://parse-server:1337/parse/classes/Area/" + area_id,
            data=json.dumps(area),
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
                "Content-Type": "application/json"
            }
        )

        return Response(resp.json(), status=resp.status_code)

    def put(self, request, *args, **kwargs):
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            print("User Connection failed")
            return Response("Unauthorized", status=401)
        area_id = kwargs.get('area_id', None)
        if area_id is None:
            return Response("Bad reaquest", status=400)
        if self.__check_user_area(area_id, user['objectId']) is None:
            print("User/Area are not ok !")
            return Response("Unauthorized", status=401)
        is_actif = request.data.get('is_actif', None)
        if is_actif is not None:
            return self.__active_desactive_area(area_id, is_actif)
        return self.__update_area(request.data, area_id)


    def delete(self, request, *args, **kwargs):
        user = utils.get_user_from_headers(request.headers)
        if user is None:
            return Response("Unauthorized", status=401)
        area_id = kwargs.get('area_id', None)
        if area_id is None:
            return Response('Need area id', status=400)
        resp = requests.get("http://parse-server:1337/parse/classes/Area",
            params={'where': json.dumps({"user_id": user['objectId'], "objectId": area_id})},
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
            }
        )

        if resp.status_code != 200:
            return Response(resp.json(), status=resp.status_code)

        if len(resp.json()['results']) == 0:
            return Response("Unauthorized action", status=401)

        resp = requests.delete("http://parse-server:1337/parse/classes/Area/" + area_id,
            headers={
                "X-Parse-Application-Id": "",
                "X-Parse-REST-API-Key": "",
            }
        )

        return Response(resp.json(), status=resp.status_code)


    def get(self, request, *args, **kwargs):
        name = kwargs.get('area_id', None)
        if name is None:
            return Response('Service not found', status=404)

        resp = requests.get('http://parse-server:1337/parse/classes/Area/' + name,
        headers={
            "X-Parse-Application-Id": "",
            "X-Parse-REST-API-Key": ""
        })

        return Response(resp.json(), status=resp.status_code)