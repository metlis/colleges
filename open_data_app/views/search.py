from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from settings import *


def search(request):
    params = request.GET

    if len(params) == 0:
        return HttpResponseRedirect(reverse('college_app:index'))
    else:
        query = request.GET['text']
        # posgres solution
        # colleges = College.objects.annotate(search=SearchVector('name', 'city', 'state__name', 'region__name'),
        #                                     ).filter(search=query)
        colleges = College.objects.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(state__name__icontains=query) | Q(region__name__icontains=query))

        if colleges.count() > 0:

            canonical = reverse('college_app:search')

            # sorting colleges
            colleges = College.sort_colleges(request, colleges)

            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # check if result is multiple
            if colleges.count() > 1:
                is_multiple = True
            else:
                is_multiple = False

            # get filters
            filters = College.get_filters(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            # a url for pagination first page
            base_url = reverse('college_app:search')

            # string for api call
            api_call = 'text={}'.format(query)

            context = {'colleges': colleges,
                       'canonical': canonical,
                       'seo_title': 'Search',
                       'base_url': base_url,
                       'params': 'text={}'.format(query),
                       'noindex': True,
                       'serach_query': query,
                       'maps_key': GOOGLE_MAPS_API,
                       'state_filter': True,
                       'api_call': api_call,
                       'is_multiple': is_multiple,
                       }

            context.update(aggregate_data)
            context.update(filters)

            return render(request, 'filtered_colleges.html', context)
        else:
            return render(request, 'filtered_colleges.html', {
                'error': True,
                'seo_title': 'Results',
                'noindex': True,
            })
