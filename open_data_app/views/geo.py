from settings import *
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.http import Http404

from open_data_app.models import State, Region
from open_data_app.models import College
from open_data_app.utils.pagination_handler import handle_pagination
from open_data_app.utils.params_handler import handle_params
from open_data_app.utils.sort_param_handler import handle_sort_param
from open_data_app.utils.params_modifier import modify_param
from open_data_app.utils.old_url_redirect_handler import handle_old_url_redirect
from open_data_app.utils.geo_redirect_handler import handle_geo_redirect
from open_data_app.utils.seo import Seo


def get_geo(request, geo_name, geo_slug):
    try:
        if geo_name == 'region':
            geo_obj = Region.objects.get(slug=geo_slug)
            region_name, slug, region_states = geo_obj.get_parsed_names()
            colleges = College.objects.filter(region=geo_obj.id).order_by('name')
            filters = College.get_filters(colleges)
        else:
            geo_obj = State.objects.get(slug=geo_slug)
            colleges = College.objects.filter(state=geo_obj.id).order_by('name')
            filters = College.get_filters(colleges, excluded_filters=['state'])
    except ObjectDoesNotExist:
        raise Http404()

    # aggregate data
    aggregate_data = College.get_aggregate_data(colleges)

    # sorting colleges
    colleges = College.sort(request, colleges)

    # sort parameters
    sort_params, active_sort_param_name, active_sort_param_val = handle_sort_param(request, is_geo_view=True)
    # sort param to insert into pagination url
    noindex = False
    if active_sort_param_val:
        active_sort_param_val = 'sort={}'.format(active_sort_param_val)
        noindex = True

    # define seo data before rendering
    seo_title = Seo.generate_title('geo_init', geo_obj.name, '')
    seo_description = Seo.generate_description('geo_init', geo_obj.name, '')

    # check if result is multiple
    is_multiple = College.check_result_is_multiple(colleges)

    # pagination
    colleges = handle_pagination(request, colleges)

    # canonical link
    canonical = reverse('college_app:geo', kwargs={'geo_name': geo_name,
                                                   'geo_slug': geo_slug, })

    # string for api call
    api_call = '{}={}'.format(geo_name, geo_obj.id)

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    context = {
               'colleges': colleges,
               'is_multiple': is_multiple,
               'version': STATIC_VERSION,
               # state data
               'slug': geo_slug,
               'view_name': 'college_app:geo_param',
               'geo_name': geo_name,
               # seo
               'seo_title': seo_title,
               'seo_description': seo_description,
               'base_url': canonical,
               'canonical': canonical,
               'noindex': noindex,
               # api
               'maps_key': GOOGLE_MAPS_API,
               'api_call': api_call,
               'favourite_colleges': favourite_colleges,
               # sort parameters
               'sort_params': sort_params,
               'active_sort_param_name': active_sort_param_name,
               'params': active_sort_param_val,
               'cookie_agreement': cookie_agreement,
               }

    if geo_name == 'region':
        context.update({
            # region data
            'region_name': region_name,
            'region_states': region_states,
            'region_id': geo_obj.id,
            'state_filter': True,
            'region_init': True,
        })
    else:
        context.update({
           # state data
           'state': geo_obj,
           'state_name': geo_obj.name,
           'state_init': True,
           'state_view': True,
        })

    context.update(filters)
    context.update(aggregate_data)

    return render(request, 'filtered_colleges.html', context)


def get_geo_param(request, geo_name, geo_slug, param_name, param_value):
    """
    Takes filters, filter values, and colleges to show on filter page

    :param request:
    :param geo_name:
    :param geo_slug:
    :param param_name: name of filter's parameter
    :param param_value: value of filter's parameter
    :return:
    """

    try:
        if geo_name == 'region':
            geo_obj = Region.objects.get(slug=geo_slug)
        else:
            geo_obj = State.objects.get(slug=geo_slug)
    except ObjectDoesNotExist:
        raise Http404()

    try:
        param_value_is_int = isinstance(int(param_value), int)
    except ValueError:
        param_value_is_int = False

    # redirecting urls with integers as parameter's values where parameter is a foreign key
    if param_value_is_int:
        redirect = handle_old_url_redirect(param_name, param_value, geo_slug, geo_name)
        if redirect:
            return redirect

    # modify parameter name if it is a discipline
    filter_param = modify_param(param_name, param_value, param_value_is_int)

    try:
        # colleges filtered by region/state + by the initial filter
        colleges = College.objects.filter(**{'{}__slug'.format(geo_name): geo_slug}).filter(
            **{filter_param: param_value}).order_by('name')
    except FieldError:
        raise Http404()

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    try:
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, geo_name, geo_obj.id)
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
        if geo_name == 'region':
            seo_name, region_slug, region_states = geo_obj.get_parsed_names()
        else:
            seo_name = geo_obj.name

        # parameter's text value and page link
        param_text_value, param_page_link = College.get_param_text_val(geo_name, geo_obj.id, param_name, param_value)

        # sorting colleges
        colleges = College.sort(request, colleges)

        # sort parameters
        sort_params, active_sort_param_name = handle_sort_param(request)

        # define seo data before rendering
        seo_template = param_name
        seo_title = Seo.generate_title(seo_template, param_text_value, seo_name)
        seo_description = Seo.generate_description(seo_template, param_text_value, seo_name)
        if param_name == 'city_slug':
            canonical = reverse('college_app:filter_values', kwargs={'param_name': param_name,
                                                                     'param_value': slugify(param_value),
                                                                     })
        else:
            canonical = reverse('college_app:geo_param', kwargs={'geo_name': geo_name,
                                                                 'geo_slug': geo_slug,
                                                                 'param_name': param_name,
                                                                 'param_value': slugify(param_value),
                                                                 })
        # state's url
        geo_page = reverse('college_app:geo', kwargs={'geo_name': geo_name,
                                                      'geo_slug': geo_slug, })

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # string for an api call
        api_call = '{}={}&{}={}&{}'.format(geo_name, geo_obj.id, param_name, param_value, req_str)

        context = {
                   'colleges': colleges,
                   'is_multiple': is_multiple,
                   'version': STATIC_VERSION,
                   # seo
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'noindex': noindex,
                   'canonical': canonical,
                   'base_url': canonical,
                   # geo data
                   '{}_id'.format(geo_name): geo_obj.id,
                   'slug': geo_slug,
                   'geo_page': geo_page,
                   'view_name': 'college_app:geo_param',
                   # initial filter
                   'init_filter_val': param_text_value,
                   'init_filter_page': param_page_link,
                   # other filters
                   'filters_vals': filters_vals,
                   # sort parameters
                   'sort_params': sort_params,
                   'active_sort_param_name': active_sort_param_name,
                   # a string with parameters
                   'params': req_str,
                    # api
                   'api_call': api_call,
                   'maps_key': GOOGLE_MAPS_API,
                   'favourite_colleges': favourite_colleges,
                   'cookie_agreement': cookie_agreement,
                   }

        if geo_name == 'region':
            context.update({
                # region data
                'region_name': seo_name,
                'geo': seo_name,
                'state_filter': True,
            })
        else:
            context.update({
               # state data
               'state': geo_obj,
               'state_name': geo_obj.name,
               'state_view': True,
               'geo': geo_obj.name,
            })

        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)

    else:
        return render(request, 'filtered_colleges.html', {
            'error': True,
            'seo_title': 'Results',
            'noindex': True,
            'favourite_colleges': favourite_colleges,
            'cookie_agreement': cookie_agreement,
            'version': STATIC_VERSION,
        })


def get_geo_redirect(request, geo_name, geo_id, geo_slug, param_name='', param_value=''):
    return handle_geo_redirect(geo_name, geo_id, geo_slug, param_name, param_value)