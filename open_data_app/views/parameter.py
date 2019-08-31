from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import FieldError
from django.http import Http404

from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.seo import Seo
from settings import *


def filter_values(request, param_name, param_value):

    try:
        param_value_is_int = isinstance(int(param_value), int)
    except ValueError:
        param_value_is_int = False

    if param_value_is_int:
        filter_param = param_name
    else:
        filter_param = '{}__slug'.format(param_name)

    try:
        # colleges filtered by the initial filter
        colleges = College.objects.filter(**{filter_param: param_value}).order_by('name')
    except FieldError:
        raise Http404()

    try:
        # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, '', '')
    except ValueError:
        raise Http404()

    if colleges.count() > 0:

        # parameter's text value
        param_text_value = College.get_param_text_val('', '', param_name, param_value)

        # define seo data before rendering
        seo_template = param_name
        seo_title = Seo.generate_title(seo_template, param_text_value, '')
        seo_description = Seo.generate_description(seo_template, param_text_value, '')
        if not 'canonical' in locals():
            canonical = reverse('college_app:filter_values', kwargs={'param_name': param_name,
                                                                     'param_value': param_value,
                                                                     })

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # check if result is multiple
        if colleges.count() > 1:
            is_multiple = True
        else:
            is_multiple = False

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # a url for pagination first page
        base_url = reverse('college_app:filter_values', kwargs={'param_name': param_name,
                                                                'param_value': param_value,
                                                                })
        # string for api call
        api_call = '{}={}&{}'.format(param_name, param_value, req_str)

        # ids of favourite colleges
        favourite_colleges = []
        if 'favourite_colleges' in request.session:
            favourite_colleges = request.session['favourite_colleges']

        context = {'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'init_filter_val': param_text_value,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'init_param': param_name,
                   'init_param_value': param_value,
                   'maps_key': GOOGLE_MAPS_API,
                   'state_filter': True,
                   'api_call': api_call,
                   'is_multiple': is_multiple,
                   'favourite_colleges': favourite_colleges,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)
    else:
        return render(request, 'filtered_colleges.html', {
            'error': True,
            'seo_title': 'Results',
            'noindex': True,
        })