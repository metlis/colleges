from settings import API_KEY, API_BASE_URL
from django.http import HttpResponse
import json


def request_scorecard_api_credentials(request):
    response = HttpResponse(
        json.dumps(
            {
                'data': {
                    'api_url': API_BASE_URL,
                    'api_key': API_KEY,
                }
            }
        ), content_type="application/json"
    )

    response['X-Robots-Tag'] = 'noindex'
    return response
