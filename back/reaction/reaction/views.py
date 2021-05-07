from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data, get_reaction_service
from rest_framework.decorators import api_view, renderer_classes
from reaction.map_reaction import MAP_REACTION
import json

def get_all_reaction_name(reactions):

    reaction_name = []

    for reaction in reactions:
        id_reaction = reaction["id"]
        reaction_name.append(id_reaction.split('-')[0])
    return reaction_name

@csrf_exempt
@api_view(('POST',))
def reaction_redirect(request, couple_id):
    print("Reaction is asked, Handle it !")

    area_data = get_reaction_data(couple_id)

    reactions = get_all_reaction_name(area_data["reaction"])

    request_data = {}
    request_data = json.loads(request.body)
    index = 0
    for reaction in reactions:
        react_fct = MAP_REACTION.get(reaction)
        react_fct(request_data, area_data, index)
        index += 1
    return Response('Reactions done', status=200)
