import re
from django.core.exceptions import FieldError
from django.db.models import Q

from open_data_app.models import College


def filter_by_params(request, colleges, entity, entity_id, main_filter=False, api_call=False):

    params = request.GET.copy()

    # string for pagination links
    req_str = ''

    # parameter's temp storage
    params_dict = {}

    # robots directive for filter pages
    noindex = False

    # delete params which are not filter params
    try:
        del params['page']
    except KeyError:
        pass

    try:
        # preserve param for url string
        req_str = 'text={}'.format(params['text'])
        del params['text']
        noindex = True
    except KeyError:
        pass

    try:
        # preserve param for url string
        sort_string = 'sort={}'.format(params['sort'])
        if req_str:
            req_str += '&{}'.format(sort_string)
        else:
            req_str = sort_string
        del params['sort']
        noindex = True
    except KeyError:
        pass

    try:
        del params['main_filter']
    except KeyError:
        pass

    if not main_filter:

        if len(params.keys()) > 0:
            noindex = True

        for key in params:
            params_dict[key] = params[key]
            if len(req_str) > 0:
                req_str += '&{}={}'.format(key, params[key])
            else:
                req_str += '{}={}'.format(key, params[key])

        try:
            new_params_dict = College.create_new_params_dict(params_dict)
            if colleges:
                colleges = colleges.filter(**new_params_dict)
            elif not colleges and api_call:
                colleges = College.objects.filter(**new_params_dict)
            else:
                colleges = College.objects.none()
        except FieldError:
            return ''

    else:
        noindex = True

        req_str = re.sub('page=(\d)+&?', '', request.META['QUERY_STRING'])

        disciplines = College.get_disciplines()
        discipline_args_list = []
        discipline_args_dict = {}
        discipline_args_query = Q()

        for key in params:
            # store discipline arguments separately to filter on them with an OR condition later
            if key in disciplines:
                discipline_args_dict[key] = params.getlist(key)
                arg = College.create_new_params_dict({key: params.getlist(key)})
                key, value = next(iter(arg.items()))
                discipline_args_list.append({key: value[0]})
            # store other arguments in a common dictionary
            else:
                params_dict[key] = params.getlist(key)

        # create a query for all disciplines arguments with an OR condition
        for arg in discipline_args_list:
            discipline_args_query = discipline_args_query | Q(**arg)

        # modify param name for the query if its value is a list
        new_params_dict = College.create_new_params_dict(params_dict)
        new_params_dict_copy = {}
        for p in new_params_dict:
            if len(new_params_dict[p]) > 1:
                if '__in' not in p:
                    new_params_dict_copy['{}__in'.format(p)] = new_params_dict[p]
                else:
                    new_params_dict_copy[p] = new_params_dict[p]
            else:
                new_params_dict_copy[p] = new_params_dict[p][0]

        # logic for queries with region and state arguments simultaneously
        new_params_dict_second_copy = new_params_dict_copy.copy()
        region_query, state_query = {}, {}

        for p in new_params_dict_copy:
            if 'region' in p or 'state' in p:
                new_params_dict_second_copy.pop(p)

            if 'region' in p:
                region_query = {p: new_params_dict_copy[p]}
            if 'state' in p:
                state_query = {p: new_params_dict_copy[p]}

        try:
            colleges = College.objects.filter(Q(**state_query) | Q(**region_query)).filter(
                **new_params_dict_second_copy).filter(*(discipline_args_query,))
        except FieldError:
            return ''

    if not api_call:
        # get applied filters text values to display on the results page
        filters_vals = []

        try:
            params_dict.update(discipline_args_dict)
        except UnboundLocalError:
            pass

        for p in params_dict:
            try:
                if isinstance(params_dict[p], list):
                    for dict_value in params_dict[p]:
                        param_text_value, param_page_link = College.get_param_text_val(entity, entity_id, p, dict_value)
                        if param_text_value:
                            filters_vals.append((param_text_value, param_page_link,))
                else:
                    param_text_value, param_page_link = College.get_param_text_val(entity, entity_id, p, params_dict[p])
                    if param_text_value:
                        filters_vals.append((param_text_value, param_page_link,))
            except Exception as e:
                print(e)
                return ''

        try:
            params_dict = new_params_dict
        except Exception as e:
            print(e)
            pass

        return colleges, req_str, noindex, filters_vals, params_dict
    else:
        return colleges
