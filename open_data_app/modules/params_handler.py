from django.http import HttpResponseNotFound

from open_data_app.models import College


def handle_params(request, colleges, entity, entity_id):
    # handle filter requests at dynamic urls
    params = request.GET
    # string used in pagination links
    req_str = ''
    # additional params used when retrieving filters
    params_dict = {}
    # robots directive for filter pages
    noindex = ''
    if len(params) == 1 and not 'page' in params:
        key = next(iter(params.keys()))
        value = next(iter(params.values()))
        params_dict[key] = value
        noindex = True
        req_str = '{}={}'.format(key, value)
        try:
            colleges = colleges.filter(**{key: value})
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    elif len(params) > 1 and 'page' in params:
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
            colleges = colleges.filter(**params_dict)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    elif len(params) > 1:
        noindex = True
        for key in params:
            params_dict[key] = params[key]
        try:
            colleges = colleges.filter(**params_dict)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    # get applied filters values to display on results page
    filters_vals = []
    for p in params_dict:
        try:
            p, val, verbose = College.get_filter_val(entity, entity_id, p, params_dict[p])
            filters_vals.append(val)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    return colleges, req_str, noindex, filters_vals, params_dict