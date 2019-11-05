from settings import GOOGLE_MAPS_API
from django.http import HttpResponse


def get_map_api_key(request):
    response = HttpResponse(GOOGLE_MAPS_API)

    response['X-Robots-Tag'] = 'noindex'
    return response