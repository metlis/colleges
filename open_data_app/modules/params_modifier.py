from open_data_app.models import College
from django.http import Http404


def modify_param(param_name, param_value, param_value_is_int):
    if param_name in College.get_disciplines():
        if param_value != '0':
            raise Http404()
        filter_param = '{}__gt'.format(param_name)
    elif param_name == 'city_slug' or param_value_is_int:
        filter_param = param_name
    else:
        filter_param = '{}__slug'.format(param_name)

    return filter_param
