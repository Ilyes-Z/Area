
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data
import smtplib
import email
from django.core.mail import EmailMessage

def mailbox(request, area_data, reaction_index):
    reaction_data = area_data["reaction"]
    params = area_data["reaction"][reaction_index]["parameters"]
    message = ""
    receiver = ""

    for param in params:
        if 'message' in param:
            message = param['message']
        elif 'receiver' in param:
            receiver = param['receiver']

    with smtplib.SMTP('smtpserver', 25) as smtp:
        smtp.send_message(email.message_from_string(message), "no-reply@are-revenge.ninja", receiver)
