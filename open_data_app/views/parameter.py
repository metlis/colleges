from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.seo import Seo



def filter_values(request, param, param_value):
    init_param = param
    # initial filter, its value, verbose name and param value
    param, query_val, verbose_name, param_value = College.get_filter_val('', '', param, param_value)

    # colleges filtered by the initial filter
    colleges = College.objects.filter(**{param: param_value}).order_by('name')

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, '', '')

    if len(colleges) > 0:

        # define seo data before rendering
        seo_template = verbose_name
        seo_title = Seo.generate_title(seo_template, query_val, '')
        seo_description = Seo.generate_description(seo_template, query_val, '')
        if not 'canonical' in locals():
            canonical = reverse('college_app:filter_values', kwargs={'param': verbose_name,
                                                                    'param_value': param_value,
                                                                    })

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # a url for pagination first page
        base_url = reverse('college_app:filter_values', kwargs={'param': verbose_name,
                                                               'param_value': param_value,
                                                               })

        # get filters
        filters = College.get_filters('', '', init_filter=param, init_filter_val=param_value, filters_set=params_dict)
        context = {'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'init_filter_val': query_val,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'init_param': init_param,
                   'init_param_value': param_value,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')