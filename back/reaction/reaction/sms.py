from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data, get_reaction_service, get_token
from rest_framework.decorators import api_view, renderer_classes
from difflib import SequenceMatcher
import json

SMS_SENDER_URL = 'https://api.smsmode.com/http/1.6/sendSMS.do'

def sms_sender(request, area_data, reaction_index):

    number = ""
    message = ""
    params = area_data["reaction"][reaction_index]["parameters"]

    for param in params:
        if 'number' in param:
            number = param['number']
        elif message in param:
            message = param('message')

    resp = requests.post(SMS_SENDER_URL, 
    data={
        'accessToken': '5Dv7HQ93jtWDXYCjicY93lHFk0eQGcuw',
        'message': message,
        'numero': number
    })

    if resp.status_code is not 200:
        raise ValueError('Error when send sms to {} number. Error: {}, Code: {}'.format(number, resp.text, resp.status_code))
