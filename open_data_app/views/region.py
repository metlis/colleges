import urllib.parse
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from open_data_app.models import Region, College, State
import re
from django.utils.text import slugify
from open_data_app.modules.seo import Seo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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
            colleges = College.objects.filter(region=region_id).order_by('name')

            filters = College.get_filters('region', region_id)
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

    canonical = reverse('college_app:region_slug', kwargs={'region_id': region_id,
                                                           'region_slug': region_slug,
                                                           })

    context = {'colleges': colleges,
               'region_name': region_name,
               'region_states': region_states,
               'region_id': region_id,
               'slug': region_slug,
               'base_url': canonical,
               'canonical': canonical,
               }

    context.update(filters)

    return render(request, 'region_colleges.html', context)


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
                    if field._verbose_name == 'state':
                        canonical = reverse('college_app:state_slug', kwargs={'state_id': rel_obj.id,
                                                                              'state_slug': slugify(rel_obj.name),
                                                                              })

            # for non-relational fields (city) get query value
            elif param in ['city_slug']:
                query_field = College.objects.filter(region__id=region_id).filter(**{param: param_value}).values(
                    field._verbose_name).distinct()
                if len(query_field) > 0:
                    query_val = query_field[0][field._verbose_name]

                    # for a city query the state view should be canonical, so
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

            colleges = College.objects.filter(region__id=region_id).filter(**{param: param_value}).order_by('name')

            # handle filter requests
            params = request.GET
            if len(params) == 1:
                key = next(iter(params.keys()))
                value = next(iter(params.values()))
                # filter_vals = College.get_filters('region', region_id, get_filter=key)
                # for val in filter_vals:
                #     if val[0] == int(value):
                #         filter_val = val[1]
                colleges = colleges.filter(**{key: value})

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
                # pagination
                if request.GET.get('page'):
                    page = request.GET.get('page')
                else:
                    page = 1
                # if parameter page does not have value all, show pagination
                if request.GET.get('page') != 'all':
                    paginator = Paginator(colleges, 50)
                    colleges = paginator.get_page(page)
                # a url for pagination first page
                base_url = reverse('college_app:region_param', kwargs={'region_id': region_id,
                                                                       'region_slug': region_slug,
                                                                       'param': field._verbose_name,
                                                                       'param_value': param_value,
                                                                       })

                # get filters
                filters = College.get_filters('region', region_id, init_filter=param, init_filter_val=param_value)
                context = {'colleges': colleges,
                           'seo_title': seo_title,
                           'canonical': canonical,
                           'base_url': base_url,
                           'init_filter_val': query_val,
                           # 'second_filter_val': filter_val,
                           }
                context.update(filters)

                return render(request, 'filtered_colleges.html', context)
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
