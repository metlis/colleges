from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from settings import *

from open_data_app.models import College
from open_data_app.utils.pagination_handler import handle_pagination
from open_data_app.utils.params_handler import handle_params
from open_data_app.utils.sort_param_handler import handle_sort_param


def search(request):
    params = request.GET

    if len(params) == 0:
        return HttpResponsePermanentRedirect(reverse('college_app:index'))
    else:
        try:
            query = request.GET['text']
        except KeyError:
            raise Http404()
        # posgres solution
        # colleges = College.objects.annotate(search=SearchVector('name', 'city', 'state__name', 'region__name'),
        #                                     ).filter(search=query)
        colleges = College.objects.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(state__name__icontains=query) | Q(region__name__icontains=query))

        try:
            # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
            # dictionary of applied filters and their values
            colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, '', '')
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

            canonical = reverse('college_app:search')

            # sorting colleges
            colleges = College.sort_colleges(request, colleges)

            # sort parameters
            sort_params, active_sort_param_name = handle_sort_param(request)

            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # check if result is multiple
            is_multiple = College.check_result_is_multiple(colleges)

            # get filters
            filters = College.get_filters(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            # a url for pagination first page
            base_url = reverse('college_app:search')

            # string for api call
            api_call = 'text={}&{}'.format(query, req_str)

            context = {'colleges': colleges,
                       'is_multiple': is_multiple,
                       # seo
                       'canonical': canonical,
                       'seo_title': 'Search',
                       'base_url': base_url,
                       'noindex': True,
                       # filters
                       'filters_vals': filters_vals,
                       'state_filter': True,
                       'serach_query': query,
                       # a string with parameters
                       'params': req_str,
                       # api
                       'api_call': api_call,
                       'maps_key': GOOGLE_MAPS_API,
                       'favourite_colleges': favourite_colleges,
                       # sort parameters
                       'sort_params': sort_params,
                       'active_sort_param_name': active_sort_param_name,
                       'cookie_agreement': cookie_agreement,
                       }

            context.update(aggregate_data)
            context.update(filters)

            return render(request, 'filtered_colleges.html', context)
        else:
            return render(request, 'filtered_colleges.html', {
                'error': True,
                'seo_title': 'Results',
                'noindex': True,
                'favourite_colleges': favourite_colleges,
                'cookie_agreement': cookie_agreement,
            })
