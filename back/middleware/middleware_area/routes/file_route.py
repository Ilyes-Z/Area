import http.client
import json
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class ApkFile(APIView):
    def get(self, request, format=None):
        file = open('requirement.txt', "rb") # to change with the app apk.
        return FileResponse(file)
