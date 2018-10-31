import urllib.parse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from open_data_app.models import Region, College
import re
from django.utils.text import slugify


def get_region(request, region_id):
    region_exist = Region.objects.filter(id=region_id).exists()

    if region_exist:
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        region_name = region_re.group(1)
        region_slug = slugify(region_name)
        return HttpResponseRedirect(urllib.parse.urljoin(str(region_id), region_slug))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')



def get_region_slug(request, region_id, region_slug):
    region_exist = Region.objects.filter(id=region_id).exists()

    if region_exist:
        region = Region.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        region_name = region_re.group(1)
        region_slug_name = slugify(region_name)
        region_states = region_re.group(2)

        if region_slug != slugify(region_slug_name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(region__id=region_id)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'region_colleges.html', {'colleges': colleges,
                                                    'region_name': region_name,
                                                    'region_states': region_states,
                                                    'slug': region_slug})