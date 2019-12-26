from open_data_app.models import Dictionary
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def get_sort_params(request, is_geo_view=False):
    try:
        sort_params = Dictionary.objects.get(name='sort_params').content
    except ObjectDoesNotExist:
        sort_params = {}

    active_sort_param_name = ''
    active_sort_param_val = ''

    if 'sort' in request.GET:
        active_sort_param_val = request.GET['sort']
        if active_sort_param_val not in list(sort_params.keys()):
            raise Http404()

        active_sort_param_name = sort_params[active_sort_param_val]

    if is_geo_view:
        return sort_params, active_sort_param_name, active_sort_param_val

    return sort_params, active_sort_param_name
