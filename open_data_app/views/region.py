from settings import *
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect

from open_data_app.models import Region, College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.seo import Seo


def get_region(request, region_slug):
    try:
        region = Region.objects.get(slug=region_slug)
        region_name, slug, region_states = region.get_region_data()

        colleges = College.objects.filter(region=region.id).order_by('name')

        filters = College.get_filters(colleges)
    except ObjectDoesNotExist:
        raise Http404()

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

    canonical = reverse('college_app:region', kwargs={'region_slug': region_slug,
                                                      })
    # string for api call
    api_call = 'region={}'.format(region.id)

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    context = {'colleges': colleges,
               'region_name': region_name,
               'region_states': region_states,
               'region_id': region.id,
               'region_slug': region.slug,
               'base_url': canonical,
               'canonical': canonical,
               'maps_key': GOOGLE_MAPS_API,
               'state_filter': True,
               'region_init': True,
               'api_call': api_call,
               'is_multiple': is_multiple,
               'favourite_colleges': favourite_colleges,
               }

    context.update(filters)
    context.update(aggregate_data)

    return render(request, 'filtered_colleges.html', context)


def get_region_param(request, region_slug, param_name, param_value):
    """
    Takes filters, filter values, and colleges to show on filter page

    :param request:
    :param region_slug:
    :param param_name: name of filter's parameter
    :param param_value: value of filter's parameter
    :return:
    """

    try:
        region = Region.objects.get(slug=region_slug)
    except ObjectDoesNotExist:
        raise Http404()

    try:
        param_value_is_int = isinstance(int(param_value), int)
    except ValueError:
        param_value_is_int = False

    # modify parameter name if it is a discipline
    if param_name in College.get_disciplines():
        filter_param = '{}__gt'.format(param_name)
    elif param_name == 'city' or param_value_is_int:
        filter_param = param_name
    else:
        filter_param = '{}__slug'.format(param_name)

    try:
        # colleges filtered by region + by the initial filter
        colleges = College.objects.filter(region__id=region.id).filter(**{filter_param: param_value}).order_by('name')
    except FieldError:
        raise Http404()

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    try:
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, 'region', region.id)
    except ValueError:
        raise Http404()

    if colleges.count() > 0:

        region_name, region_slug, region_states = region.get_region_data()

        # parameter's text value
        param_text_value = College.get_param_text_val('region', region.id, param_name, param_value)

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # define seo data before rendering
        seo_template = param_name
        seo_title = Seo.generate_title(seo_template, param_text_value, region_name)
        seo_description = Seo.generate_description(seo_template, param_text_value, region_name)
        if not 'canonical' in locals():
            canonical = reverse('college_app:region_param', kwargs={'region_slug': region.slug,
                                                                    'param_name': param_name,
                                                                    'param_value': slugify(param_value),
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
        base_url = reverse('college_app:region_param', kwargs={'region_slug': region.slug,
                                                               'param_name': param_name,
                                                               'param_value': slugify(param_value),
                                                               })

        # string for api call
        api_call = 'region={}&{}={}&{}'.format(region.id, param_name, param_value, req_str)

        # ids of favourite colleges
        favourite_colleges = []
        if 'favourite_colleges' in request.session:
            favourite_colleges = request.session['favourite_colleges']

        context = {
                   'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': base_url,
                   'region_id': region.id,
                   'region_slug': region.slug,
                   'init_filter_val': param_text_value,
                   'geo': region_name,
                   'second_filter': param_text_value,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'maps_key': GOOGLE_MAPS_API,
                   'state_filter': True,
                   'api_call': api_call,
                   'is_multiple': is_multiple,
                   'favourite_colleges': favourite_colleges,
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


def get_region_redirect(request, region_id, region_slug, param_name='', param_value=''):
    try:
        region = Region.objects.get(id=region_id)

        if region_slug != region.slug:
            raise Http404()
        else:
            if not param_name and not param_value:
                return HttpResponsePermanentRedirect(reverse('college_app:region', kwargs={
                    'region_slug': region_slug,
                }))
            else:
                return HttpResponsePermanentRedirect(reverse('college_app:region_param', kwargs={
                    'region_slug': region_slug,
                    'param_name': param_name,
                    'param_value': param_value,
                }))
    except ObjectDoesNotExist:
        raise Http404()