from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data, get_reaction_service

@require_POST
@csrf_exempt
def reddit_parser(request, area_data, reaction_index):
    area_data = get_reaction_data(couple_id)

    service_data = get_reaction_service(area_data["reaction"]["id"])
