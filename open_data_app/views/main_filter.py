from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from settings import *


def main_filter(request):
    params = request.GET

    canonical = reverse('college_app:main_filter')

    # a url for pagination first page
    base_url = reverse('college_app:main_filter')

    if len(params) > 0:
        # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
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

            # check if result is multiple
            if colleges.count() > 1:
                is_multiple = True
            else:
                is_multiple = False

            # get filters
            filters = College.get_filters(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            context = {'colleges': colleges,
                       'seo_title': 'Results',
                       'canonical': canonical,
                       'base_url': base_url,
                       'params': req_str,
                       'noindex': noindex,
                       'filters_vals': filters_vals,
                       'main_filter': True,
                       'maps_key': GOOGLE_MAPS_API,
                       'state_filter': True,
                       'api_call': req_str,
                       'is_multiple': is_multiple,
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
        try:
            sort = request.GET['sort']
            if sort:
                colleges = colleges.order_by(sort)
        except:
            pass

        # check if result is multiple
        if colleges.count() > 1:
            is_multiple = True
        else:
            is_multiple = False

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        context = {'colleges': colleges,
                   'seo_title': 'USA College and University search',
                   'seo_description': 'You can use filters on this page to search between more than 7,000 american universities and colleges in 50 states. The information on this web site is provided by College Scorecard.',
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': False,
                   'maps_key': GOOGLE_MAPS_API,
                   'state_filter': True,
                   'api_call': '',
                   'is_multiple': is_multiple,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)