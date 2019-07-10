from django.shortcuts import render
from open_data_app.models import College
from django.utils.text import slugify
from django.http import HttpResponseNotFound, HttpResponseRedirect
import urllib.parse
from settings import *


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
        if request.session.get('visited_colleges') is None:
            request.session['visited_colleges'] = ()

        request.session['visited_colleges'] += (college_id,)

        college = College.objects.get(id=college_id)

        disciplines = College.get_disciplines()

        disciplines_vals = []

        dict = College.get_dict()

        for disc in disciplines:
            val = getattr(college, disc)
            try:
                if float(val) > 0:
                    val_formatted = float("{0:.2f}".format(val * 100))
                    disciplines_vals.append([dict[disc], val_formatted])
            except:
                pass

        top_disciplines = sorted(disciplines_vals, key=lambda x: x[1], reverse=True)

        if college_slug != slugify(college.name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return render(request, 'college.html', {'college': college,
                                                    'college_id': college_id,
                                                    'college_slug': college_slug,
                                                    'top_disciplines': top_disciplines[:5],
                                                    'college_disciplines': disciplines_vals,
                                                    'maps_key': GOOGLE_MAPS_API,
                                                    })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
