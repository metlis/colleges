import urllib.parse
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from open_data_app.models import Region, College, State
import re
from django.utils.text import slugify
from open_data_app.modules.seo import Seo


def get_region(request, region_id):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        params = request.GET
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        try:
            region_name = region_re.group(1)
            region_slug = slugify(region_name)
        except:
            region_slug = ''

        if len(params) == 0:
            return HttpResponseRedirect(urllib.parse.urljoin(str(region_id), region_slug))
        # static address for url with one parameter
        elif len(params) == 1:
            key = next(iter(params.keys()))
            value = next(iter(params.values()))

            try:
                verbose_name = College._meta.get_field(key).verbose_name
                url = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                  'region_slug': region_slug,
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


def get_region_slug(request, region_id, region_slug):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        try:
            region_name = region_re.group(1)
            region_slug_name = slugify(region_name)
            region_states = region_re.group(2)
        except:
            region_name = ''
            region_slug_name = ''
            region_states = ''

        if region_slug != slugify(region_slug_name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(region__id=region_id)
            colleges_cities = College.objects.filter(region=region_id).values_list('city',
                                                                                   'city_slug').order_by(
                'city').distinct()
            colleges_states = College.objects.filter(region=region_id).values_list('state__id',
                                                                                   'state__name').order_by(
                'state__name').distinct()
            colleges_ownership = College.objects.filter(region=region_id).values_list('ownership__id',
                                                                                      'ownership__description').order_by(
                'ownership__id').distinct()
            colleges_locales = College.objects.filter(region=region_id).values_list('locale__id',
                                                                                    'locale__description').order_by(
                'locale__id').exclude(
                locale__description=None).distinct()
            colleges_degrees = College.objects.filter(region=region_id).values_list('highest_grad_degree__id',
                                                                                    'highest_grad_degree__description').order_by(
                'highest_grad_degree__id').distinct()
            colleges_carnegie_basic = College.objects.filter(region=region_id).values_list('carnegie_basic__code_num',
                                                                                           'carnegie_basic__description').order_by(
                'carnegie_basic__code_num').exclude(carnegie_basic__description=None).exclude(
                carnegie_basic__description='Not applicable').distinct()
            colleges_religions = College.objects.filter(region=region_id).values_list('religous__id',
                                                                                      'religous__name').order_by(
                'religous__name').exclude(religous__name=None).distinct()
            colleges_levels = College.objects.filter(region=region_id).values_list('inst_level__id',
                                                                                   'inst_level__description').order_by(
                'inst_level__id').distinct()
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'region_colleges.html', {'colleges': colleges,
                                                    'region_name': region_name,
                                                    'region_states': region_states,
                                                    'region_id': region_id,
                                                    'slug': region_slug,
                                                    'cities': colleges_cities,
                                                    'states': colleges_states,
                                                    'ownerships': colleges_ownership,
                                                    'locales': colleges_locales,
                                                    'degrees': colleges_degrees,
                                                    'basics': colleges_carnegie_basic,
                                                    'religions': colleges_religions,
                                                    'levels': colleges_levels,
                                                    })


def get_region_param(request, region_id, region_slug, param, param_value):
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
    region_name = Region.objects.get(id=region_id).name

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


                    # assign canonical if the field is state
                    if  field._verbose_name == 'state':
                        canonical = reverse('college_app:state_slug', kwargs={'state_id': rel_obj.id,
                                                                               'state_slug': slugify(rel_obj.name),
                                                                               })

            # for non-relational fields (city) get query value
            else:
                query_field = College.objects.filter(region__id=region_id).filter(**{param: param_value}).values(
                    field._verbose_name).distinct()
                if len(query_field) > 0:
                    query_val = query_field[0][field._verbose_name]

                    # state view for cities should be canonical, so
                    # get the first college to define the state
                    college = College.objects.filter(region__id=region_id).filter(**{param: param_value})[0]
                    state = State.objects.get(id=college.state.id)
                    state_id = state.id
                    state_slug = slugify(state.name)
                    canonical = reverse('college_app:state_param', kwargs={'state_id': state_id,
                                                                           'state_slug': state_slug,
                                                                           'param': field._verbose_name,
                                                                           'param_value': param_value,
                                                                           })
                else:
                    return HttpResponseNotFound('<h1>Page not found</h1>')

            colleges = College.objects.filter(region__id=region_id).filter(**{param: param_value})

            if len(colleges) > 0:

                # define seo data before rendering
                seo_template = field._verbose_name
                seo_title = Seo.generate_title(seo_template, query_val, region_name)
                if not 'canonical' in locals():
                    canonical = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                            'region_slug': region_slug,
                                                                            'param': field._verbose_name,
                                                                            'param_value': param_value,
                                                                            })

                return render(request, 'filtered_colleges.html', {'colleges': colleges,
                                                                  'seo_title': seo_title,
                                                                  'canonical': canonical,
                                                                  })
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
