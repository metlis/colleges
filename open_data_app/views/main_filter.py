from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params


def main_filter(request):
    params = request.GET

    if len(params) == 0:
        return HttpResponseRedirect(reverse('college_app:index'))
    else:
        colleges = College.objects.all()

        # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, '', '')

        if len(colleges) > 0:
            canonical = reverse('college_app:main_filter')

            # pagination
            colleges = handle_pagination(request, colleges)

            # a url for pagination first page
            base_url = reverse('college_app:main_filter')

            # get filters
            filters = College.get_filters('', '', filters_set=params_dict)

            context = {'colleges': colleges,
                       'canonical': canonical,
                       'base_url': base_url,
                       'params': req_str,
                       'noindex': noindex,
                       'filters_vals': filters_vals,
                       }
            context.update(filters)

            return render(request, 'filtered_colleges.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')