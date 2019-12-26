from django.http import HttpResponse
from open_data_app.models import College
from open_data_app.utils.params_handler import filter_by_params
import json
from django.db.models import Q
from htmlmin.decorators import not_minified_response


@not_minified_response
def request_map_labels(request):
    params = request.GET

    if 'text' in params:
        colleges = College.objects.filter(Q(name__icontains=params['text']) | Q(city__icontains=params['text']) | Q(state__name__icontains=params['text']) | Q(region__name__icontains=params['text']))
        colleges = filter_by_params(request, colleges, '', '', main_filter=False, api_call=True)
    elif 'main_filter' in params:
        colleges = filter_by_params(request, '', '', '', main_filter=True, api_call=True)
    elif 'rating_ids' in params:
        colleges = College.objects.filter(id__in=params['rating_ids'].split(','))
    else:
        colleges = filter_by_params(request, '', '', '', main_filter=False, api_call=True)

    # map labels
    map_labels = College.get_map_labels(colleges)

    response = HttpResponse(
        json.dumps(
            {
                'data': map_labels
            }
        ), content_type="application/json"
    )

    response['X-Robots-Tag'] = 'noindex'
    return response
