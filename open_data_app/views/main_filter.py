from django.http import HttpResponseRedirect, HttpResponseNotFound
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

    colleges = College.objects.all()

    if len(params) > 0:
        # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, '', '', main_filter=True)


        if len(colleges) > 0:
            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # sorting colleges
            colleges = College.sort_colleges(request, colleges)

            # map labels
            map_labels = College.get_map_labels(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            # get filters
            filters = College.get_filters('', '', filters_set=params_dict)

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
                       'map_labels': map_labels,
                       }
            context.update(filters)
            context.update(aggregate_data)

            return render(request, 'filtered_colleges.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # sorting colleges
        try:
            sort = request.GET['sort']
            if sort:
                colleges = colleges.order_by(sort)
        except:
            pass


        # map labels
        map_labels = College.get_map_labels(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # get filters
        filters = College.get_filters('', '')

        context = {'colleges': colleges,
                   'seo_title': 'Results',
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': True,
                   'maps_key': GOOGLE_MAPS_API,
                   'state_filter': True,
                   'map_labels': map_labels,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)