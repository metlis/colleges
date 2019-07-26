from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from open_data_app.models import Region, College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.seo import Seo
from settings import *


def get_region(request, region_id, region_slug):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        region = Region.objects.get(id=region_id)
        region_name, slug, region_states = region.get_region_data()

        params = request.GET

        if region_slug != slug:
            return render(request, 'filtered_colleges.html', {
                'error': True,
                'seo_title': 'Results',
                'noindex': True,
            })
        # static address for url with single parameter
        elif len(params) == 1 and not 'page' in params:
            key = next(iter(params.keys()))
            value = next(iter(params.values()))

            try:
                verbose_name = College._meta.get_field(key).verbose_name
                url = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                  'region_slug': region_slug,
                                                                  'param': verbose_name,
                                                                  'param_value': value,
                                                                  })
                return HttpResponseRedirect(url)
            except:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(region=region_id).order_by('name')

            filters = College.get_filters(colleges)
    else:
        return render(request, 'filtered_colleges.html', {
            'error': True,
            'seo_title': 'Results',
            'noindex': True,
        })

    # aggregate data
    aggregate_data = College.get_aggregate_data(colleges)

    # sorting colleges
    colleges = College.sort_colleges(request, colleges)

    # check if result is multiple
    if colleges.count() > 1:
        is_multiple = True
    else:
        is_multiple = False

    # pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    # if parameter page does not have value all, show pagination
    if request.GET.get('page') != 'all':
        paginator = Paginator(colleges, 50)
        colleges = paginator.get_page(page)

    canonical = reverse('college_app:region', kwargs={'region_id': region_id,
                                                           'region_slug': region_slug,
                                                           })
    # string for api call
    api_call = 'region={}'.format(region_id)

    context = {'colleges': colleges,
               'region_name': region_name,
               'region_states': region_states,
               'region_id': region_id,
               'region_slug': region_slug,
               'base_url': canonical,
               'canonical': canonical,
               'maps_key': GOOGLE_MAPS_API,
               'state_filter': True,
               'region_init': True,
               'api_call': api_call,
               'is_multiple': is_multiple,
               }

    context.update(filters)
    context.update(aggregate_data)

    return render(request, 'filtered_colleges.html', context)


def get_region_param(request, region_id, region_slug, param, param_value):
    """
    Searches field by verbose name and takes its value. Works for any filter page

    :param request:
    :param region_id:
    :param region_slug:
    :param param: verbose name of a field
    :param param_value: value of a field
    :return:
    """
    region = Region.objects.get(id=region_id)
    region_name, region_slug, region_states = region.get_region_data()

    # initial filter, its value, verbose name and param value
    param, query_val, verbose_name, param_value = College.get_filter_val('region', region_id, param, param_value)

    # modify filter if it is about disciplines
    disciplines = College.get_disciplines()
    if param in disciplines:
        filter_param = '{}__gt'.format(param)
    else:
        filter_param = param

    # colleges filtered by the initial filter + by region
    colleges = College.objects.filter(region__id=region_id).filter(**{filter_param: param_value}).order_by('name')

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, 'region', region_id)

    if colleges.count() > 0:

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # define seo data before rendering
        seo_template = verbose_name
        seo_title = Seo.generate_title(seo_template, query_val, region_name)
        seo_description = Seo.generate_description(seo_template, query_val, region_name)
        if not 'canonical' in locals():
            canonical = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                    'region_slug': region_slug,
                                                                    'param': verbose_name,
                                                                    'param_value': param_value,
                                                                    })
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
        base_url = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                               'region_slug': region_slug,
                                                               'param': verbose_name,
                                                               'param_value': param_value,
                                                               })

        # string for api call
        api_call = 'region={}&{}={}&{}'.format(region_id, param, param_value, req_str)

        context = {
                   'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'region_id': region_id,
                   'region_slug': region_slug,
                   'init_filter_val': query_val,
                   'geo': region_name,
                   'second_filter': query_val,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'maps_key': GOOGLE_MAPS_API,
                   'state_filter': True,
                   'api_call': api_call,
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
