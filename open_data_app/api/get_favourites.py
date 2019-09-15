from open_data_app.models import College

from django.http import HttpResponse
import json


def get_favourites(request):
    college_ids = request.session.get('favourite_colleges')

    if college_ids is not None:
        colleges = College.objects.filter(id__in=college_ids).values()
    else:
        colleges = []

    return HttpResponse(
        json.dumps(
            {
                'data': list(colleges)
            }
        ), content_type="application/json")
