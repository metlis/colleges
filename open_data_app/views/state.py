from settings import *
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect

from open_data_app.models import State
from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from open_data_app.modules.sort_param_handler import handle_sort_param
from open_data_app.modules.seo import Seo


def get_state(request, state_slug):
    try:
        state = State.objects.get(slug=state_slug)
        colleges = College.objects.filter(state=state.id).order_by('name')
        filters = College.get_filters(colleges, excluded_filters=['state'])
    except ObjectDoesNotExist:
        raise Http404()

    # aggregate data
    aggregate_data = College.get_aggregate_data(colleges)

    # sorting colleges
    colleges = College.sort_colleges(request, colleges)

    # sort parameters
    sort_params, active_sort_param_name, active_sort_param_val = handle_sort_param(request, is_geo_view=True)
    # sort param to insert into pagination url
    if active_sort_param_val:
        active_sort_param_val = 'sort={}'.format(active_sort_param_val)

    # define seo data before rendering
    seo_title = Seo.generate_title('geo_init', state.name, '')
    seo_description = Seo.generate_description('geo_init', state.name, '')

    # check if result is multiple
    is_multiple = College.check_result_is_multiple(colleges)

    # pagination
    colleges = handle_pagination(request, colleges)

    # canonical link
    canonical = reverse('college_app:state', kwargs={'state_slug': state_slug,})

    # string for api call
    api_call = 'state={}'.format(state.id)

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    context = {
               'colleges': colleges,
               'is_multiple': is_multiple,
               # state data
               'state': state,
               'state_name': state.name,
               'state_slug': state.slug,
               'state_init': True,
               'state_view': True,
               # seo
               'seo_title': seo_title,
               'seo_description': seo_description,
               'base_url': canonical,
               'canonical': canonical,
               # api
               'maps_key': GOOGLE_MAPS_API,
               'api_call': api_call,
               'favourite_colleges': favourite_colleges,
               # sort parameters
               'sort_params': sort_params,
               'active_sort_param_name': active_sort_param_name,
               'params': active_sort_param_val,
               }

    context.update(filters)
    context.update(aggregate_data)

    return render(request, 'filtered_colleges.html', context)


def get_state_param(request, state_slug, param_name, param_value):
    """
    Takes filters, filter values, and colleges to show on filter page

    :param request:
    :param state_slug:
    :param param_name: name of filter's parameter
    :param param_value: value of filter's parameter
    :return:
    """

    try:
        state = State.objects.get(slug=state_slug)
    except ObjectDoesNotExist:
        raise Http404()

    try:
        param_value_is_int = isinstance(int(param_value), int)
    except ValueError:
        param_value_is_int = False

    # redirecting urls with integers as parameter's values where parameter is a foreign key
    if param_value_is_int:
        if param_name not in College.get_binary_params() and param_name not in College.get_disciplines():
            param_slug_value = College.get_param_slug_val(param_name, param_value)
            if param_slug_value:
                return HttpResponsePermanentRedirect(reverse('college_app:state_param', kwargs={
                    'state_slug': state_slug,
                    'param_name': param_name,
                    'param_value': param_slug_value,
                }))

    # modify parameter name if it is a discipline
    if param_name in College.get_disciplines():
        filter_param = '{}__gt'.format(param_name)
    elif param_name == 'city_slug' or param_value_is_int:
        filter_param = param_name
    else:
        filter_param = '{}__slug'.format(param_name)

    try:
        # colleges filtered by state + by the initial filter
        colleges = College.objects.filter(state__slug=state.slug).filter(**{filter_param: param_value}).order_by('name')
    except FieldError:
        raise Http404()

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    try:
        colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, 'state', state.id)
    except ValueError:
        raise Http404()

    if colleges.count() > 0:

        # parameter's text value and page link
        param_text_value, param_page_link = College.get_param_text_val('state', state.id, param_name, param_value)

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # sort parameters
        sort_params, active_sort_param_name = handle_sort_param(request)

        # define seo data before rendering
        seo_template = param_name
        seo_title = Seo.generate_title(seo_template, param_text_value, state.name)
        seo_description = Seo.generate_description(seo_template, param_text_value, state.name)
        canonical = reverse('college_app:state_param', kwargs={'state_slug': state.slug,
                                                               'param_name': param_name,
                                                               'param_value': slugify(param_value),
                                                               })
        # state's url
        state_page = reverse('college_app:state', kwargs={'state_slug': state_slug, })

        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = handle_pagination(request, colleges)

        # string for an api call
        api_call = 'state={}&{}={}&{}'.format(state.id, param_name, param_value, req_str)

        # ids of favourite colleges
        favourite_colleges = []
        if 'favourite_colleges' in request.session:
            favourite_colleges = request.session['favourite_colleges']

        context = {
                   'colleges': colleges,
                   'is_multiple': is_multiple,
                   # seo
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'noindex': noindex,
                   'canonical': canonical,
                   'base_url': canonical,
                   # state data
                   'state_id': state.id,
                   'state_slug': state.slug,
                   'state_name': state.name,
                   'state_view': True,
                   'geo': state.name,
                   'geo_page': state_page,
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


def get_state_redirect(request, state_id, state_slug, param_name='', param_value=''):
    try:
        state = State.objects.get(id=state_id)

        if state_slug != state.slug:
            raise Http404()
        else:
            if not param_name and not param_value:
                return HttpResponsePermanentRedirect(reverse('college_app:state', kwargs={
                    'state_slug': state_slug,
                }))
            else:
                return HttpResponsePermanentRedirect(reverse('college_app:state_param', kwargs={
                    'state_slug': state_slug,
                    'param_name': param_name,
                    'param_value': param_value,
                }))
    except ObjectDoesNotExist:
        raise Http404()