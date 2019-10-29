from settings import GOOGLE_MAPS_API
from django.http import HttpResponse


def get_map_api_key(request):
    return HttpResponse(GOOGLE_MAPS_API)