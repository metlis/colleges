from open_data_app.models import Dictionary
from django.core.exceptions import ObjectDoesNotExist


def handle_sort_param(request):
    try:
        sort_params = Dictionary.objects.get(name='sort_params').content
    except ObjectDoesNotExist:
        sort_params = {}

    active_sort_param_name = ''
    if 'sort' in request.GET:
        active_sort_param = request.GET['sort']
        active_sort_param_name = sort_params[active_sort_param]

    return sort_params, active_sort_param_name
