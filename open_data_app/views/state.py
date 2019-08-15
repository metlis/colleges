from django.shortcuts import render
from django.urls import reverse
from open_data_app.models import State
from open_data_app.models import College
from open_data_app.modules.pagination_handler import handle_pagination
from open_data_app.modules.params_handler import handle_params
from settings import *
from open_data_app.modules.seo import Seo
from django.core.paginator import Paginator


def get_state(request, state_id, state_slug):
    state_exists = State.objects.filter(id=state_id).exists()

    if state_exists:
        state = State.objects.get(id=state_id)
        slug = state.get_state_slug()

        if state_slug != slug:
            return render(request, 'filtered_colleges.html', {
                'error': True,
                'seo_title': 'Results',
                'noindex': True,
            })
        else:
            colleges = College.objects.filter(state=state_id).order_by('name')

            filters = College.get_filters(colleges, excluded_filters=['state'])
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

    canonical = reverse('college_app:state', kwargs={'state_id': state_id,
                                                          'state_slug': state_slug,
                                                          })
    # string for api call
    api_call = 'state={}'.format(state.id)

    context = {
               'colleges': colleges,
               'state': state,
               'state_id': state_id,
               'state_name': state.name,
               'state_slug': state_slug,
               'base_url': canonical,
               'canonical': canonical,
               'maps_key': GOOGLE_MAPS_API,
               'state_init': True,
               'state_view': True,
               'api_call': api_call,
               'is_multiple': is_multiple,
               }

    context.update(filters)
    context.update(aggregate_data)

    return render(request, 'filtered_colleges.html', context)


def get_state_param(request, state_id, state_slug, param, param_value):
    """
    Takes filters, filter values, and colleges to show on filter page

    :param request:
    :param state_id:
    :param state_slug:
    :param param: verbose name of a field
    :param param_value: value of a field
    :return:
    """
    state_name = State.objects.get(id=state_id).name

    # initial filter, its value, verbose name and param value
    param, query_val, verbose_name, param_value = College.get_filter_val('state', state_id, param, param_value)

    # modify filter if it is about disciplines
    disciplines = College.get_disciplines()
    if param in disciplines:
        filter_param = '{}__gt'.format(param)
    else:
        filter_param = param

    # colleges filtered by the initial filter + by state
    colleges = College.objects.filter(state__id=state_id).filter(**{filter_param: param_value}).order_by('name')

    # colleges filtered by secondary filters, request string for rendering links, readable values of applied filters and
    # dictionary of applied filters and their values
    colleges, req_str, noindex, filters_vals, params_dict = handle_params(request, colleges, 'state', state_id)


    if colleges.count() > 0:

        # sorting colleges
        colleges = College.sort_colleges(request, colleges)

        # define seo data before rendering
        seo_template = verbose_name
        seo_title = Seo.generate_title(seo_template, query_val, state_name)
        seo_description = Seo.generate_description(seo_template, query_val, state_name)
        canonical = reverse('college_app:state_param', kwargs={'state_id': state_id,
                                                               'state_slug': state_slug,
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


        # string for api call
        api_call = 'state={}&{}={}&{}'.format(state_id, param, param_value, req_str)

        context = {
                    'colleges': colleges,
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'canonical': canonical,
                   'base_url': canonical,
                   'state_view': True,
                   'state_id': state_id,
                   'state_slug': state_slug,
                   'init_filter_val': query_val,
                   'geo': state_name,
                   'second_filter': query_val,
                   'params': req_str,
                   'noindex': noindex,
                   'filters_vals': filters_vals,
                   'maps_key': GOOGLE_MAPS_API,
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

