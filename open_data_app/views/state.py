from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from open_data_app.models import State
from open_data_app.models import College
from settings import *
import urllib.parse
from open_data_app.modules.seo import Seo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_state(request, state_id):
    state_exists = State.objects.filter(id=state_id).exists()

    if state_exists:
        params = request.GET
        state, state_slug = State.get_state_data(state_id)

        if len(params) == 0:
            return HttpResponseRedirect(urllib.parse.urljoin(str(state_id), state_slug))
        # static address for url with one parameter
        elif len(params) == 1:
            key = next(iter(params.keys()))
            value = next(iter(params.values()))

            try:
                verbose_name = College._meta.get_field(key).verbose_name
                url = reverse('college_app:state_param', kwargs={'state_id': state_id,
                                                                 'state_slug': state_slug,
                                                                 'param': verbose_name,
                                                                 'param_value': value,
                                                                 })
                return HttpResponseRedirect(url)
            except:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return HttpResponse('In development')

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def get_state_slug(request, state_id, state_slug):
    state_exists = State.objects.filter(id=state_id).exists()

    if state_exists:
        state, slug = State.get_state_data(state_id)

        if state_slug != slug:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(state=state_id).order_by('name')

            filters = College.get_filters('state', state_id, 'states')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    # if parameter page does not have value all, show pagination
    if request.GET.get('page') != 'all':
        paginator = Paginator(colleges, 50)
        colleges = paginator.get_page(page)

    canonical = reverse('college_app:state_slug', kwargs={'state_id': state_id,
                                                          'state_slug': state_slug,
                                                          })

    context = {'colleges': colleges,
               'state': state,
               'state_id': state_id,
               'name': state.name,
               'slug': state_slug,
               'base_url': canonical,
               'canonical': canonical,
               }

    context.update(filters)

    return render(request, 'state_colleges.html', context)


def get_state_param(request, state_id, state_slug, param, param_value):
    """
    Searches field by verbose name and takes its value. Works for any filter page

    :param request:
    :param state_id:
    :param state_slug:
    :param param: verbose name of a field
    :param param_value: value of a field
    :return:
    """
    college_fields = College._meta.get_fields()
    state_name = State.objects.get(id=state_id).name

    for field in college_fields:
        if param == field._verbose_name:

            # if verbose name and name are different, change query param to name of the field
            if param != field.attname:
                param = field.attname

            # for relational fields get related object
            if field.related_model is not None:
                rel_obj_exists = field.related_model.objects.filter(pk=param_value).exists()

                if rel_obj_exists:
                    rel_obj = field.related_model.objects.get(pk=param_value)

                    # get relational field text value
                    try:
                        query_val = rel_obj.description
                    except:
                        query_val = rel_obj.name

            # for non-relational fields (city) get query value
            elif param in ['city_slug']:
                query_field = College.objects.filter(state__id=state_id).filter(**{param: param_value}).values(
                    field._verbose_name).distinct()
                if len(query_field) > 0:
                    query_val = query_field[0][field._verbose_name]
                else:
                    return HttpResponseNotFound('<h1>Page not found</h1>')
            # yes/no queries
            else:
                dict = {'hist_black': ['Historically not black', 'Historically black'],
                        'predom_black': ['Predominantely not black', 'Predominantely black'],
                        'hispanic': ['Predominantely not hispanic', 'Predominantely hispanic'],
                        'men_only': ['Not men-only', 'Men-only'],
                        'women_only': ['Not women-only', 'Women-only'],
                        'online_only': ['Not online-only', 'Online-only'],
                        'cur_operating': ['Currently closed', 'Currently operating'],
                        }

                query_val = dict[param][int(param_value)]

            colleges = College.objects.filter(state__id=state_id).filter(**{param: param_value}).order_by('name')

            # handle filter requests
            params = request.GET
            # string used in pagination links
            req_str = ''
            # additional params used when retrieving filters
            params_dict = {}
            if len(params) == 1 and not 'page' in params:
                key = next(iter(params.keys()))
                value = next(iter(params.values()))
                params_dict[key] = value
                req_str = '{}={}'.format(key, value)
                try:
                    colleges = colleges.filter(**{key: value})
                except:
                    return HttpResponseNotFound('<h1>Page not found</h1>')
            elif len(params) > 1 and 'page' in params:
                req = params.copy()
                del req['page']
                req_str = ''
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
                for key in params:
                    params_dict[key] = params[key]
                try:
                    colleges = colleges.filter(**params_dict)
                except:
                    return HttpResponseNotFound('<h1>Page not found</h1>')


            if len(colleges) > 0:

                # define seo data before rendering
                seo_template = field._verbose_name
                seo_title = Seo.generate_title(seo_template, query_val, state_name)
                canonical = reverse('college_app:state_param', kwargs={'state_id': state_id,
                                                                       'state_slug': state_slug,
                                                                       'param': field._verbose_name,
                                                                       'param_value': param_value,
                                                                       })

                # pagination
                if request.GET.get('page'):
                    page = request.GET.get('page')
                else:
                    page = 1
                # if parameter page does not have value all, show pagination
                if request.GET.get('page') != 'all':
                    paginator = Paginator(colleges, 50)
                    colleges = paginator.get_page(page)
                # get filters
                filters = College.get_filters('state', state_id, excluded_filters=['state'], init_filter=param, init_filter_val=param_value, filters_set=params_dict)
                context = {'colleges': colleges,
                           'seo_title': seo_title,
                           'canonical': canonical,
                           'base_url': canonical,
                           'state_view': True,
                           'state_id': state_id,
                           'geo': state_name,
                           'second_filter': query_val,
                           'params': req_str,
                           }
                context.update(filters)

                return render(request, 'filtered_colleges.html', context)

            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
