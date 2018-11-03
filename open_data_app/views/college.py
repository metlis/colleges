from django.shortcuts import render
from open_data_app.models import College
from django.utils.text import slugify
from django.http import HttpResponseNotFound, HttpResponseRedirect
import urllib.parse


def get_college(request, college_id):
    college_exists = College.objects.filter(id=college_id).exists()

    if college_exists:
        college = College.objects.get(id=college_id)
        college_slug = slugify(college.name)
        return HttpResponseRedirect(urllib.parse.urljoin(str(college_id), college_slug))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def get_college_slug(request, college_id, college_slug):
    college_exists = College.objects.filter(id=college_id).exists()

    if college_exists:
        college = College.objects.get(id=college_id)

        if college_slug != slugify(college.name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return render(request, 'college.html', {'college': college})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
