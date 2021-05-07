import http.client
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib
import requests
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from django.views.decorators.csrf import csrf_exempt

@api_view(('POST',))
@require_POST
@csrf_exempt
def parse_hook(request, service_name, couple_id):
    if service_name is None or couple_id is None:
        return Response('Service name and couple id are required.', status=status.HTTP_400_BAD_REQUEST)
    
    content = {}
    try:
        request.body
    except:
        data = {
            "service_name": service_name,
            "couple_id": couple_id,
            }
    else:
        data = {
            "data": json.loads(request.body),
            "service_name": service_name,
            "couple_id": couple_id,
            }
    print("Tigger {} service ! Send to rection !".format(service_name))
    resp = requests.post("http://reaction:6060/react/{}".format(couple_id),json=data)

    return Response(resp.text, status=resp.status_code)
