from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import FieldError
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from open_data_app.models import College, Dictionary
from open_data_app.utils.old_url_redirect_handler import make_old_url_redirect
from open_data_app.utils.pagination_handler import create_paginator
from open_data_app.utils.params_handler import filter_by_params
from open_data_app.utils.seo import Seo
from open_data_app.utils.sort_param_handler import get_sort_params
from open_data_app.utils.get_aggregate_filter_text_from_colleges import get_aggregate_filter_text_from_colleges
from settings import *


def filter_values(request, param_name, param_value):

    try:
        disciplines = Dictionary.objects.get(name='discipline_slugs').content
    except ObjectDoesNotExist:
        disciplines = []
    if param_name in disciplines:
        raise Http404()

    try:
        param_value_is_int = isinstance(int(param_value), int)
    except ValueError:
        param_value_is_int = False

    # redirecting urls with integers as parameter's values where parameter is a foreign key
    if param_value_is_int:
        redirect = make_old_url_redirect(param_name, param_value)
        if redirect:
            return redirect

    if param_value_is_int or param_name == 'city_slug':
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
        colleges, req_str, noindex, filters_vals, params_dict = filter_by_params(request, colleges, '', '')
    except ValueError:
        raise Http404()

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    if colleges.count() > 0:

        # parameter's text value and page link
        param_text_value, param_page_link = College.get_param_text_val('', '', param_name, param_value)

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

        # text with aggregate information for pages without get parameters
        aggregate_text = get_aggregate_filter_text_from_colleges(request, colleges)

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # sorting colleges
        colleges = College.sort(request, colleges)

        # sort parameters
        sort_params, active_sort_param_name = get_sort_params(request)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = create_paginator(request, colleges)

        # a url for pagination first page
        base_url = reverse('college_app:filter_values', kwargs={'param_name': param_name,
                                                                'param_value': param_value,
                                                                })
        # string for api call
        api_call = '{}={}&{}'.format(param_name, param_value, req_str)

        context = {'colleges': colleges,
                   'is_multiple': is_multiple,
                   'version': STATIC_VERSION,
                   'aggregate_text': aggregate_text,
                   # seo
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': noindex,
                   # initial filter
                   'init_filter_val': param_text_value,
                   'init_param': param_name,
                   'init_param_value': param_value,
                   # other filters
                   'filters_vals': filters_vals,
                   'state_filter': True,
                   # a string with parameters
                   'params': req_str,
                   # sort parameters
                   'sort_params': sort_params,
                   'active_sort_param_name': active_sort_param_name,
                    # api
                   'api_call': api_call,
                   'gmaps_key': GOOGLE_MAPS_API,
                   'ymaps_key': YANDEX_MAPS_API,
                   'map_api_vendor': MAP_API_VENDOR,
                   'favourite_colleges': favourite_colleges,
                   'cookie_agreement': cookie_agreement,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)
    else:
        return render(request, 'filtered_colleges.html', {
            'error': True,
            'seo_title': 'Results',
            'noindex': True,
            'favourite_colleges': favourite_colleges,
            'cookie_agreement': cookie_agreement,
            'version': STATIC_VERSION,
        })