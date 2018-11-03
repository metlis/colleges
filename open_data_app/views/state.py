from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from open_data_app.models import State
from open_data_app.models import College
from settings import *
from django.utils.text import slugify
import urllib.parse

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
            colleges = College.objects.filter(state__id=state_id)
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
            colleges_carnegie_basic = College.objects.filter(state=state_id).values_list('carnegie_basic__code_num',
                                                                                         'carnegie_basic__description').order_by(
                'carnegie_basic__code_num').exclude(carnegie_basic__description=None).exclude(
                carnegie_basic__description='Not applicable').distinct()
            colleges_religions = College.objects.filter(state=state_id).values_list('religous__id',
                                                                                    'religous__name').order_by(
                'religous__name').exclude(religous__name=None).distinct()
            colleges_levels = College.objects.filter(state=state_id).values_list('inst_level__id',
                                                                                 'inst_level__description').order_by(
                'inst_level__id').distinct()

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'state_colleges.html', {'colleges': colleges,
                                                   'state': state,
                                                   'slug': state_slug,
                                                   'cities': colleges_cities,
                                                   'ownerships': colleges_ownership,
                                                   'locales': colleges_locales,
                                                   'degrees': colleges_degrees,
                                                   'basics': colleges_carnegie_basic,
                                                   'religions': colleges_religions,
                                                   'levels': colleges_levels,
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

    for field in college_fields:
        if param == field._verbose_name:

            # if verbose name and name are different, change query param to name of the field
            if param != field.attname:
                param = field.attname

            # for relational fields get related object
            rel_obj_exists = field.related_model.objects.filter(pk=param_value).exists()

            if rel_obj_exists:
                rel_obj = field.related_model.objects.get(pk=param_value)

                try:
                    rel_obj_val = rel_obj.description
                except:
                    rel_obj_val = rel_obj.name

            colleges = College.objects.filter(state__id=state_id).filter(**{param: param_value})

            if len(colleges) > 0:
                return render(request, 'filtered_colleges.html', {'colleges': colleges,
                                                              'rel_obj_val': rel_obj_val
                                                              })

            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
