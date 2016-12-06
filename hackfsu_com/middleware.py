"""
    Custom Middleware
"""

from django.http import JsonResponse
import json


class JsonLoader(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            try:
                request.JSON = json.loads(request.body.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                return JsonResponse({
                    "error": "Invalid JSON request"
                })

        return self.get_response(request)
