from open_data_app.models import College

from django.http import HttpResponse
import json


def request_user_colleges(request):
    college_fields = [f.name for f in College._meta.get_fields()]
    college_fields += ['state__name', 'carnegie__description', 'degree__description', 'level__description',
                       'locale__description', 'ownership__description', 'region__name', 'religion__name']

    favourite_colleges_ids = request.session.get('favourite_colleges')
    visited_colleges_ids = request.session.get('visited_colleges')

    filtered_colleges = {
        'favourite': [],
        'visited': [],
    }

    if favourite_colleges_ids is not None:
        filtered_colleges['favourite'] = College.objects.filter(id__in=favourite_colleges_ids).values(*college_fields)

    if visited_colleges_ids is not None:
        filtered_colleges['visited'] = College.objects.filter(id__in=visited_colleges_ids).values(*college_fields)

    response = HttpResponse(
        json.dumps(
            {
                'data': {
                    'favourite': list(filtered_colleges['favourite']),
                    'visited': list(filtered_colleges['visited']),
                }
            }
        ), content_type="application/json")

    response['X-Robots-Tag'] = 'noindex'
    return response
