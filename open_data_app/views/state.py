from settings import *
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect

from open_data_app.models import State
from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
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

    canonical = reverse('college_app:state', kwargs={'state_slug': state_slug,})
    # string for api call
    api_call = 'state={}'.format(state.id)

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    context = {
               'colleges': colleges,
               'state': state,
               'state_name': state.name,
               'state_slug': state.slug,
               'base_url': canonical,
               'canonical': canonical,
               'maps_key': GOOGLE_MAPS_API,
               'state_init': True,
               'state_view': True,
               'api_call': api_call,
               'is_multiple': is_multiple,
               'favourite_colleges': favourite_colleges,
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


    # modify parameter name if it is a discipline
    if param_name in College.get_disciplines():
        filter_param = '{}__gt'.format(param_name)
    else:
        filter_param = param_name

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

        # parameter's text value
        param_text_value = College.get_param_text_val('state', state.id, param_name, param_value)

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # define seo data before rendering
        seo_template = param_name
        seo_title = Seo.generate_title(seo_template, param_text_value, state.name)
        seo_description = Seo.generate_description(seo_template, param_text_value, state.name)
        canonical = reverse('college_app:state_param', kwargs={'state_slug': state.slug,
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

        # string for an api call
        api_call = 'state={}&{}={}&{}'.format(state.id, param_name, param_value, req_str)

        # ids of favourite colleges
        favourite_colleges = []
        if 'favourite_colleges' in request.session:
            favourite_colleges = request.session['favourite_colleges']

        context = {
                   'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': canonical,
                   'state_view': True,
                   'state_id': state.id,
                   'state_slug': state.slug,
                   'init_filter_val': param_text_value,
                   'geo': state.name,
                   'second_filter': param_text_value,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'maps_key': GOOGLE_MAPS_API,
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