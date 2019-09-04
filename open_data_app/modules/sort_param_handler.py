from open_data_app.models import Dictionary
from django.core.exceptions import ObjectDoesNotExist


def handle_sort_param(request, is_geo_view=False):
    try:
        sort_params = Dictionary.objects.get(name='sort_params').content
    except ObjectDoesNotExist:
        sort_params = {}

    active_sort_param_name = ''
    active_sort_param_val = ''

    if 'sort' in request.GET:
        active_sort_param_val = request.GET['sort']
        active_sort_param_name = sort_params[active_sort_param_val]

    if is_geo_view:
        return sort_params, active_sort_param_name, active_sort_param_val

    return sort_params, active_sort_param_name
