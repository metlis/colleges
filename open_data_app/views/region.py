import urllib.parse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from open_data_app.models import Region, College
import re
from django.utils.text import slugify


def get_region(request, region_id):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        region_name = region_re.group(1)
        region_slug = slugify(region_name)
        return HttpResponseRedirect(urllib.parse.urljoin(str(region_id), region_slug))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def get_region_slug(request, region_id, region_slug):
    region_exists = Region.objects.filter(id=region_id).exists()

    if region_exists:
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        region_name = region_re.group(1)
        region_slug_name = slugify(region_name)
        region_states = region_re.group(2)

        if region_slug != slugify(region_slug_name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(region__id=region_id)
            colleges_cities = College.objects.filter(region=region_id).values('city').distinct()
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
