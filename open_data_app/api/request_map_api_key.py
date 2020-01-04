from settings import GOOGLE_MAPS_API, YANDEX_MAPS_API, MAP_API_VENDOR
from django.http import HttpResponse
import json


def request_map_api_key(request):
    if MAP_API_VENDOR == 'Google':
        response = HttpResponse(
            json.dumps(
                {
                    'key': GOOGLE_MAPS_API,
                    'vendor': 'google',
                }
            ), content_type="application/json")
    else:
        response = HttpResponse(
            json.dumps(
                {
                    'key': YANDEX_MAPS_API,
                    'vendor': 'ymaps',
                }
            ), content_type="application/json")

    response['X-Robots-Tag'] = 'noindex'
    return response
