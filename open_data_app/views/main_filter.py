from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.sort_param_handler import handle_sort_param
from settings import *


def main_filter(request):
    params = request.GET

    canonical = reverse('college_app:main_filter')

    # a url for pagination first page
    base_url = reverse('college_app:main_filter')

    if len(params) > 0:
        # filtered colleges, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        try:
            colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, '', '', '', main_filter=True)
        except ValueError:
            raise Http404()

        if colleges.count() > 0:
            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # sorting colleges
            colleges = College.sort_colleges(request, colleges)

            # sort parameters
            sort_params, active_sort_param_name = handle_sort_param(request)

            # check if result is multiple
            is_multiple = College.check_result_is_multiple(colleges)

            # get filters
            filters = College.get_filters(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            # ids of favourite colleges
            favourite_colleges = []
            if 'favourite_colleges' in request.session:
                favourite_colleges = request.session['favourite_colleges']

            context = {'colleges': colleges,
                       'is_multiple': is_multiple,
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
                       'maps_key': GOOGLE_MAPS_API,
                       'favourite_colleges': favourite_colleges,
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
            })
    else:
        colleges = College.objects.all()

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # sort parameters
        sort_params, active_sort_param_name = handle_sort_param(request)

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # ids of favourite colleges
        favourite_colleges = []
        if 'favourite_colleges' in request.session:
            favourite_colleges = request.session['favourite_colleges']

        context = {'colleges': colleges,
                   'is_multiple': is_multiple,
                   # seo
                   'seo_title': 'USA College and University search',
                   'seo_description': 'You can use filters on this page to search between more than 7,000 american universities and colleges in 50 states. The information on this web site is provided by College Scorecard.',
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': False,
                   # api
                   'maps_key': GOOGLE_MAPS_API,
                   'api_call': '',
                   'favourite_colleges': favourite_colleges,
                   # filter
                   'state_filter': True,
                   # sort parameters
                   'sort_params': sort_params,
                   'active_sort_param_name': active_sort_param_name,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)