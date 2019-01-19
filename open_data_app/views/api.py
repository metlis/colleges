from django.http import HttpResponse
from open_data_app.models import College
from open_data_app.modules.params_handler import handle_params
import json
from django.db.models import Q
from htmlmin.decorators import not_minified_response


@not_minified_response
def api(request):
    params = request.GET
    try:
        colleges = College.objects.filter(Q(name__icontains=params['text']) | Q(city__icontains=params['text']) | Q(state__name__icontains=params['text']) | Q(region__name__icontains=params['text']))
    except:
        colleges = handle_params(request, '', '', '', main_filter=True, api_call=True)
    # map labels
    map_labels = College.get_map_labels(colleges)

    return HttpResponse(
        json.dumps(
            {
                'data': map_labels
            }
        )
    )
