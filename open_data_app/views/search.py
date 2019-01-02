from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params

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
        colleges = College.objects.annotate(search=SearchVector('name', 'city', 'state__name', 'region__name'),
                                            ).filter(search=query)

        if len(colleges) > 0:

            canonical = reverse('college_app:search')

            # sorting colleges
            colleges = College.sort_colleges(request, colleges)

            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # pagination
            colleges = handle_pagination(request, colleges)

            # a url for pagination first page
            base_url = reverse('college_app:search')

            context = {'colleges': colleges,
                       'canonical': canonical,
                       'seo_title': 'Search',
                       'base_url': base_url,
                       'params': 'text={}'.format(query),
                       'noindex': True,
                       'serach_query': query,
                       'maps_key': GOOGLE_MAPS_API,
                       }

            context.update(aggregate_data)

            return render(request, 'filtered_colleges.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
