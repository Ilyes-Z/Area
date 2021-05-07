#!/bin/python3

import os
import http.client
import json
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class DownloadApp(APIView):
    def get(self, request, format=None):
        path = os.getenv("AREA_APP_PATH")
        file = None
        try :
            file = open(path, "rb")
        except :
            return HttpResponseNotFound("<h1>File not found</h1>")
        return FileResponse(file, as_attachment=True, filename="area.apk")
