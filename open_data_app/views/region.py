import urllib.parse
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from open_data_app.models import Region, College, State
from django.utils.text import slugify

from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.seo import Seo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_region(request, region_id):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        params = request.GET
        region_name, region_slug, region_states = Region.get_region_data(region_id)

        if len(params) == 0:
            return HttpResponseRedirect(urllib.parse.urljoin(str(region_id), region_slug))
        # static address for url with one parameter
        elif len(params) == 1:
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
            return HttpResponse('In development')

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def get_region_slug(request, region_id, region_slug):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        region_name, slug, region_states = Region.get_region_data(region_id)

        if region_slug != slug:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(region=region_id).order_by('name')

            filters = College.get_filters('region', region_id)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    # if parameter page does not have value all, show pagination
    if request.GET.get('page') != 'all':
        paginator = Paginator(colleges, 50)
        colleges = paginator.get_page(page)

    canonical = reverse('college_app:region_slug', kwargs={'region_id': region_id,
                                                           'region_slug': region_slug,
                                                           })

    context = {'colleges': colleges,
               'region_name': region_name,
               'region_states': region_states,
               'region_id': region_id,
               'slug': region_slug,
               'base_url': canonical,
               'canonical': canonical,
               }

    context.update(filters)

    return render(request, 'region_colleges.html', context)


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
    region_name, region_slug, region_states = Region.get_region_data(region_id)

    # initial filter, its value and verbose name
    param, query_val, verbose_name = College.get_filter_val('region', region_id, param, param_value)

    # colleges filtered by the initial filter + by region
    colleges = College.objects.filter(region__id=region_id).filter(**{param: param_value}).order_by('name')

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, 'region', region_id)



    if len(colleges) > 0:

        # define seo data before rendering
        seo_template = verbose_name
        seo_title = Seo.generate_title(seo_template, query_val, region_name)
        if not 'canonical' in locals():
            canonical = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                    'region_slug': region_slug,
                                                                    'param': verbose_name,
                                                                    'param_value': param_value,
                                                                    })
        # pagination
        colleges = handle_pagination(request, colleges)

        # a url for pagination first page
        base_url = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                               'region_slug': region_slug,
                                                               'param': verbose_name,
                                                               'param_value': param_value,
                                                               })

        # get filters
        filters = College.get_filters('region', region_id, init_filter=param, init_filter_val=param_value, filters_set=params_dict)
        context = {'colleges': colleges,
                   'seo_title': seo_title,
                   'canonical': canonical,
                   'base_url': base_url,
                   'region_id': region_id,
                   'init_filter_val': query_val,
                   'geo': region_name,
                   'second_filter': query_val,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   }
        context.update(filters)

        return render(request, 'filtered_colleges.html', context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

