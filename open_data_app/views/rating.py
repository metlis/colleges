from open_data_app.models.rating import Rating
from open_data_app.models.college import College
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render

from open_data_app.utils.params_handler import filter_by_params
from settings import *

from open_data_app.utils.pagination_handler import create_paginator
from open_data_app.utils.sort_param_handler import get_sort_params
from open_data_app.utils.get_aggregate_filter_text_from_colleges import get_aggregate_filter_text_from_colleges


def create_rating(request, rating_url):
    if not Rating.objects.filter(url=rating_url).exists():
        raise Http404()

    rating = Rating.objects.get(url=rating_url)
    rating_filters = rating.filters
    colleges = College.objects.all()
    # filtering colleges by rating's filters
    for f in rating_filters.all():
        if f.parameter_name:
            colleges = colleges.filter(**{f.parameter_name: f.parameter_value})

        if f.state:
            colleges = colleges.filter(state=f.state)

        if f.region:
            colleges = colleges.filter(region=f.region)

        if f.ownership:
            colleges = colleges.filter(ownership=f.ownership)

        if f.locale:
            colleges = colleges.filter(locale=f.locale)

        if f.degree:
            colleges = colleges.filter(degree=f.degree)

        if f.carnegie:
            colleges = colleges.filter(carnegie=f.carnegie)

        if f.religion:
            colleges = colleges.filter(religion=f.religion)

        if f.level:
            colleges = colleges.filter(level=f.level)

        if f.order:
            order_field_name = f.order
            if f.order.startswith('-'):
                order_field_name = f.order[1:]
            is_null_param = '{}__isnull'.format(order_field_name)
            colleges = colleges.filter(**{is_null_param: False}).order_by(f.order)

        if f.items_quantity:
            sliced_colleges_ids = [c.id for c in colleges[0:f.items_quantity]]
            colleges = colleges.filter(id__in=sliced_colleges_ids)

    # canonical page
    canonical = reverse('college_app:create_rating', kwargs={'rating_url': rating_url})

    # a url for pagination first page
    base_url = reverse('college_app:create_rating', kwargs={'rating_url': rating_url})

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    # seo
    seo_title = rating.title
    seo_description = rating.description
    rating_header = rating.name

    params = request.GET
    # filtering colleges by filters applied on rating's page
    if len(params) > 0:
        # filtered colleges, request string for rendering links, readable values of applied filters and
        # dictionary of applied filters and their values
        try:
            colleges, req_str, noindex, filters_vals, params_dict = filter_by_params(request, colleges, '', '')
        except ValueError:
            raise Http404()

        if colleges.count() > 0:
            # aggregate data
            aggregate_data = College.get_aggregate_data(colleges)

            # sorting colleges
            colleges = College.sort(request, colleges)

            # sort parameters
            sort_params, active_sort_param_name = get_sort_params(request)

            # check if result is multiple
            is_multiple = College.check_result_is_multiple(colleges)

            # get filters
            filters = College.get_filters(colleges)

            # api
            api_call = College.create_api_call_string_from_ids(colleges)

            # pagination
            colleges = create_paginator(request, colleges)

            context = {'colleges': colleges,
                       'is_multiple': is_multiple,
                       'version': STATIC_VERSION,
                       # seo
                       'seo_title': seo_title,
                       'seo_description': seo_description,
                       'canonical': canonical,
                       'base_url': base_url,
                       'params': req_str,
                       'noindex': noindex,
                       'rating_header': rating_header,
                       'rating_url': rating_url,
                       # filters
                       'filters_vals': filters_vals,
                       # api
                       'api_call': api_call,
                       'maps_key': GOOGLE_MAPS_API,
                       'favourite_colleges': favourite_colleges,
                       'cookie_agreement': cookie_agreement,
                       # sort parameters
                       'sort_params': sort_params,
                       'active_sort_param_name': active_sort_param_name,
                       }
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
    else:
        # aggregate data
        aggregate_data = College.get_aggregate_data(colleges)

        # text with aggregate information for pages without get parameters
        aggregate_text = get_aggregate_filter_text_from_colleges(request, colleges)

        # api
        api_call = College.create_api_call_string_from_ids(colleges)

        # sort parameters
        sort_params, active_sort_param_name = get_sort_params(request)

        # check if result is multiple
        is_multiple = College.check_result_is_multiple(colleges)

        # get filters
        filters = College.get_filters(colleges)

        # pagination
        colleges = create_paginator(request, colleges)

        context = {'colleges': colleges,
                   'is_multiple': is_multiple,
                   'version': STATIC_VERSION,
                   'aggregate_text': aggregate_text,
                   # seo
                   'seo_title': seo_title,
                   'seo_description': seo_description,
                   'rating_header': rating_header,
                   'rating_url': rating_url,
                   'canonical': canonical,
                   'base_url': base_url,
                   'noindex': False,
                   # api
                   'maps_key': GOOGLE_MAPS_API,
                   'api_call': api_call,
                   'favourite_colleges': favourite_colleges,
                   'cookie_agreement': cookie_agreement,
                   # sort parameters
                   'sort_params': sort_params,
                   'active_sort_param_name': active_sort_param_name,
                   }
        context.update(filters)
        context.update(aggregate_data)

        return render(request, 'filtered_colleges.html', context)