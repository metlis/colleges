from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from open_data_app.models import College
from open_data_app.utils.pagination_handler import create_paginator
from open_data_app.utils.params_handler import filter_by_params
from open_data_app.utils.seo import Seo
from open_data_app.utils.sort_param_handler import get_sort_params
from open_data_app.utils.text_generators import generate_filter_text
from settings import *


def main_filter(request):
    params = request.GET

    canonical = reverse('college_app:main_filter')

    # a url for pagination first page
    base_url = reverse('college_app:main_filter')

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    if len(params) > 0:
        # filtered colleges, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        try:
            colleges, req_str, noindex, filters_vals, params_dict = filter_by_params(request, '', '', '', main_filter=True)
        except ValueError:
            raise Http404()

        if colleges.count() > 0:
            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # sorting colleges
            colleges = College.sort(request, colleges)

            # sort parameters
            sort_params, active_sort_param_name = get_sort_params(request)

            # check if result is multiple
            is_multiple = College.check_result_is_multiple(colleges)

            # get filters
            filters = College.get_filters(colleges)

            # pagination
            colleges = create_paginator(request, colleges)

            context = {'colleges': colleges,
                       'is_multiple': is_multiple,
                       'version': STATIC_VERSION,
                       # seo
                       'seo_title': 'Results',
                       'canonical': canonical,
                       'base_url': base_url,
                       'params': req_str,
                       'noindex': noindex,
                       # filters
                       'filters_vals': filters_vals,
                       'main_filter': True,
                       'state_filter': True,
                       # api
                       'api_call': req_str + '&main_filter=1',
                       'gmaps_key': GOOGLE_MAPS_API,
                       'ymaps_key': YANDEX_MAPS_API,
                       'map_api_vendor': MAP_API_VENDOR,
                       'favourite_colleges': favourite_colleges,
                       'cookie_agreement': cookie_agreement,
                       # sort parameters
                       'sort_params': sort_params,
                       'active_sort_param_name': active_sort_param_name,
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
    else:
        colleges = College.objects.all()

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # sort parameters
        sort_params, active_sort_param_name = get_sort_params(request)

        # define seo data before rendering
        seo_title = Seo.generate_title('main', '', '')
        seo_description = Seo.generate_description('main', '', '')

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = create_paginator(request, colleges)

        # text with aggregate information
        aggregate_text = generate_filter_text()

        context = {'colleges': colleges,
                   'is_multiple': is_multiple,
                   'version': STATIC_VERSION,
                   'aggregate_text': aggregate_text,
                   # seo
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': False,
                   # api
                   'gmaps_key': GOOGLE_MAPS_API,
                   'ymaps_key': YANDEX_MAPS_API,
                   'map_api_vendor': MAP_API_VENDOR,
                   'api_call': 'main_filter=1',
                   'favourite_colleges': favourite_colleges,
                   'cookie_agreement': cookie_agreement,
                   # filter
                   'state_filter': True,
                   # sort parameters
                   'sort_params': sort_params,
                   'active_sort_param_name': active_sort_param_name,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)