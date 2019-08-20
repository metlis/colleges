import re
from django.core.exceptions import FieldError

from open_data_app.models import College


def handle_params(request, colleges, entity, entity_id, main_filter=False, api_call=False):
    # handle filter requests at dynamic urls
    params = request.GET

    # exclude sort parameter if any
    params_temp = params.copy()
    params_temp.pop('sort', None)
    params = params_temp

    # string used in pagination links
    req_str = ''

    # additional params used when retrieving filters
    params_dict = {}

    # robots directive for filter pages
    noindex = ''

    disciplines = College.get_disciplines()

    if len(params) == 1 and not 'page' in params and not main_filter and not api_call:
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
        except FieldError:
            return ''
    elif len(params) > 1 and 'page' in params and not main_filter and not api_call:
        req = params.copy()
        del req['page']
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
        except FieldError:
            return ''
    elif len(params) > 1 and not main_filter and not api_call:
        noindex = True
        for key in params:
            params_dict[key] = params[key]
            if len(req_str) > 0:
                req_str += '&{}={}'.format(key, params[key])
            else:
                req_str += '{}={}'.format(key, params[key])
        try:
            new_params_dict = College.create_new_params_dict(params_dict)
            colleges = colleges.filter(**new_params_dict)
        except FieldError:
            return ''
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

        # logic for queries with region and state at the same time
        region_query = ''
        state_query = ''
        for p in new_params_dict:
            if 'region' in p:
                region_param = p
                region_query = {p: new_params_dict[p]}
            if 'state' in p:
                state_param = p
                state_query = {p: new_params_dict[p]}

        if region_query and state_query:
            try:
                state_colleges = College.objects.filter(**state_query)
                region_colleges = College.objects.filter(**region_query)
                colleges = (state_colleges | region_colleges).distinct()
                param_dict_copy = new_params_dict.copy()
                param_dict_copy.pop(region_param)
                param_dict_copy.pop(state_param)
                if len(param_dict_copy) > 0:
                    colleges = College.objects.filter(**param_dict_copy)
            except FieldError:
                pass
        else:
            try:
                colleges = College.objects.filter(**new_params_dict)
            except FieldError:
                return ''

    if not api_call:
        # get applied filters values to display on results page
        filters_vals = []
        for p in params_dict:
            try:
                if isinstance(params_dict[p], list):
                    for dict_value in params_dict[p]:
                        param_text_value = College.get_param_text_val(entity, entity_id, p, dict_value)
                        filters_vals.append(param_text_value)
                else:
                    param_text_value = College.get_param_text_val(entity, entity_id, p, params_dict[p])
                    filters_vals.append(param_text_value)

            except:
                return ''

        try:
            params_dict = new_params_dict
        except:
            pass

        return colleges, req_str, noindex, filters_vals, params_dict
    else:
        return colleges