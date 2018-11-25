from django.http import HttpResponseNotFound
from open_data_app.models import College
import re


def handle_params(request, colleges, entity, entity_id, main_filter=False):
    # handle filter requests at dynamic urls
    params = request.GET
    # params copy to modify
    req = params.copy()

    # string used in pagination links
    req_str = ''

    # additional params used when retrieving filters
    params_dict = {}

    # robots directive for filter pages
    noindex = ''

    disciplines = College.get_disciplines()

    if len(params) == 1 and not 'page' in params and not main_filter:
        key = next(iter(params.keys()))
        value = next(iter(params.values()))
        params_dict[key] = value
        noindex = True
        req_str = '{}={}'.format(key, value)
        try:
            # modify academics query param
            if key in disciplines:
                new_key = '{}__gt'.format(key)
            else:
                new_key = key
            colleges = colleges.filter(**{new_key: value})
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    elif len(params) > 1 and 'page' in params and not main_filter:
        req = params.copy()
        del req['page']
        req_str = ''
        noindex = True
        for key in req:
            params_dict[key] = req[key]
            if len(req_str) > 0:
                req_str += '&{}={}'.format(key, req[key])
            else:
                req_str += '{}={}'.format(key, req[key])
        try:
            new_params_dict = College.create_new_params_dict(params_dict)
            colleges = colleges.filter(**new_params_dict)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    elif len(params) > 1 and not main_filter:
        noindex = True
        for key in params:
            params_dict[key] = params[key]
        try:
            new_params_dict = College.create_new_params_dict(params_dict)
            colleges = colleges.filter(**new_params_dict)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    elif main_filter:
        req_str = re.sub('page=(\d)+&?', '', request.META['QUERY_STRING'])
        noindex = True

        for key in params:
            if key != 'page':
                params_dict[key] = params.getlist(key)

        # modify param name for the query if its value is a list
        new_params_dict = College.create_new_params_dict(params_dict)
        for p in new_params_dict:
            if len(new_params_dict[p]) > 1:
                if not '__in' in p:
                    new_params_dict['{}__in'.format(p)] = new_params_dict.pop(p)
            else:
                new_params_dict[p] = new_params_dict[p][0]

        try:
            colleges = colleges.filter(**new_params_dict)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')



    # get applied filters values to display on results page
    filters_vals = []
    for p in params_dict:
        try:
            if isinstance(params_dict[p], list):
                for dict_value in params_dict[p]:
                    pr, val, verbose, param_value = College.get_filter_val(entity, entity_id, p, dict_value)
                    filters_vals.append(val)
            else:
                p, val, verbose, param_value = College.get_filter_val(entity, entity_id, p, params_dict[p])
                filters_vals.append(val)

        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    try:
        params_dict = new_params_dict
    except:
        pass

    return colleges, req_str, noindex, filters_vals, params_dict