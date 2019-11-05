from open_data_app.models import College

from django.http import HttpResponse
import json


def get_favourites(request):
    college_ids = request.session.get('favourite_colleges')

    if college_ids is not None:
        college_fields = [f.name for f in College._meta.get_fields()]
        college_fields += ['state__name', 'carnegie__description', 'degree__description', 'level__description',
                           'locale__description', 'ownership__description', 'region__name', 'religion__name']
        colleges = College.objects.filter(id__in=college_ids).values(*college_fields)
    else:
        colleges = []

    response = HttpResponse(
        json.dumps(
            {
                'data': list(colleges)
            }
        ), content_type="application/json")

    response['X-Robots-Tag'] = 'noindex'
    return response
