from open_data_app.models import College

from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


def handle_old_url_redirect(param_name, param_value, slug, geo):
    if param_name not in College.get_binary_params() and param_name not in College.get_disciplines():
        param_slug_value = College.get_param_slug_val(param_name, param_value)
        if param_slug_value:
            return HttpResponsePermanentRedirect(reverse('college_app:{}_param'.format(geo), kwargs={
                '{}_slug'.format(geo): slug,
                'param_name': param_name,
                'param_value': param_slug_value,
            }))

    return ''
