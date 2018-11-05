from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from open_data_app.models import State
from open_data_app.models import College
from settings import *
from django.utils.text import slugify
import urllib.parse
from open_data_app.modules.seo import Seo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_state(request, state_id):
    state_exists = State.objects.filter(id=state_id).exists()

    if state_exists:
        params = request.GET
        state = State.objects.get(id=state_id)
        state_slug = slugify(state.name)

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
        state = State.objects.get(id=state_id)

        if state_slug != slugify(state.name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(state__id=state_id).order_by('name')
            colleges_cities = College.objects.filter(state=state_id).values_list('city',
                                                                                 'city_slug').order_by(
                'city').distinct()
            colleges_ownership = College.objects.filter(state=state_id).values_list('ownership__id',
                                                                                    'ownership__description').order_by(
                'ownership__id').distinct()
            colleges_locales = College.objects.filter(state=state_id).values_list('locale__id',
                                                                                  'locale__description').order_by(
                'locale__id').exclude(
                locale__description=None).distinct()
            colleges_degrees = College.objects.filter(state=state_id).values_list('highest_grad_degree__id',
                                                                                  'highest_grad_degree__description').order_by(
                'highest_grad_degree__id').distinct()
            colleges_carnegie_basic = College.objects.filter(state=state_id).values_list('carnegie_basic__id',
                                                                                         'carnegie_basic__description').order_by(
                'carnegie_basic__description').exclude(carnegie_basic__description=None).exclude(
                carnegie_basic__description='Not applicable').distinct()
            colleges_religions = College.objects.filter(state=state_id).values_list('religous__id',
                                                                                    'religous__name').order_by(
                'religous__name').exclude(religous__name=None).distinct()
            colleges_levels = College.objects.filter(state=state_id).values_list('inst_level__id',
                                                                                 'inst_level__description').order_by(
                'inst_level__id').distinct()
            colleges_hist_black = College.objects.filter(state=state_id).values('hist_black').distinct()
            colleges_predom_black = College.objects.filter(state=state_id).values('predom_black').distinct()
            colleges_hispanic = College.objects.filter(state=state_id).values('hispanic').distinct()
            colleges_men_only = College.objects.filter(state=state_id).values('men_only').distinct()
            colleges_women_only = College.objects.filter(state=state_id).values('women_only').distinct()
            colleges_online_only = College.objects.filter(state=state_id).values('online_only').distinct()
            colleges_cur_operating = College.objects.filter(state=state_id).values('cur_operating').distinct()

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

    return render(request, 'state_colleges.html', {'colleges': colleges,
                                                   'state': state,
                                                   'state_id': state_id,
                                                   'slug': state_slug,
                                                   'cities': colleges_cities,
                                                   'ownerships': colleges_ownership,
                                                   'locales': colleges_locales,
                                                   'degrees': colleges_degrees,
                                                   'basics': colleges_carnegie_basic,
                                                   'religions': colleges_religions,
                                                   'levels': colleges_levels,
                                                   'colleges_hist_black': colleges_hist_black,
                                                   'colleges_predom_black': colleges_predom_black,
                                                   'colleges_hispanic': colleges_hispanic,
                                                   'colleges_men_only': colleges_men_only,
                                                   'colleges_women_only': colleges_women_only,
                                                   'colleges_online_only': colleges_online_only,
                                                   'colleges_cur_operating': colleges_cur_operating,
                                                   'base_url': canonical,
                                                   'canonical': canonical,
                                                   })


def get_state_param(request, state_id, state_slug, param, param_value):
    """
    Searches field by verbose name and takes its value. Works for any single-parameter filter page

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

                return render(request, 'filtered_colleges.html', {'colleges': colleges,
                                                                  'seo_title': seo_title,
                                                                  'canonical': canonical,
                                                                  'base_url': canonical,
                                                                  })

            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
