import re
from django.core.exceptions import FieldError

from open_data_app.models import College


def handle_params(request, colleges, entity, entity_id, main_filter=False, api_call=False):

    params = request.GET.copy()

    try:
        del params['page']
    except KeyError:
        pass

    try:
        del params['text']
    except KeyError:
        pass

    try:
        del params['sort']
    except KeyError:
        pass

    # string for pagination links
    req_str = ''

    # parameter's temp storage
    params_dict = {}

    # robots directive for filter pages
    noindex = ''

    if not main_filter:

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

    else:
        req_str = re.sub('page=(\d)+&?', '', request.META['QUERY_STRING'])
        noindex = True

        for key in params:
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
                state_query = {'{}__slug'.format(p): new_params_dict[p]}

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
        # get applied filters text values to display on the results page
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
            except Exception as e:
                print(e)
                return ''

        try:
            params_dict = new_params_dict
        except:
            pass

        return colleges, req_str, noindex, filters_vals, params_dict
    else:
        return colleges