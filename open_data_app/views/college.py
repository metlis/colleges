from django.shortcuts import render
from open_data_app.models import College
from django.utils.text import slugify
from django.http import Http404
from settings import *


def get_college(request, college_id, college_slug):
    college_exists = College.objects.filter(id=college_id).exists()

    if college_exists:
        college = College.objects.get(id=college_id)

        if college_slug != slugify(college.name):
            raise Http404()

        else:
            if request.session.get('visited_colleges') is None:
                request.session['visited_colleges'] = []
            request.session['visited_colleges'] = list(set(request.session['visited_colleges'] + [college.id]))

            is_favourite = False
            if request.session.get('favourite_colleges') is not None \
                    and str(college.id) in request.session['favourite_colleges']:
                is_favourite = True

            disciplines = College.get_disciplines()

            disciplines_vals = []

            dictionary = College.get_dict()

            for d in disciplines:
                val = getattr(college, d)
                try:
                    if float(val) > 0:
                        val_formatted = float("{0:.2f}".format(val * 100))
                        disciplines_vals.append([dictionary[d], val_formatted])
                except:
                    pass

            top_disciplines = sorted(disciplines_vals, key=lambda x: x[1], reverse=True)

            # referring page's url for the back button
            referer = request.META.get('HTTP_REFERER')

            return render(request, 'college.html', {'college': college,
                                                    'top_disciplines': top_disciplines[:5],
                                                    'college_disciplines': disciplines_vals,
                                                    'is_favourite': is_favourite,
                                                    'maps_key': GOOGLE_MAPS_API,
                                                    'referer': referer,
                                                    })
    else:
        raise Http404()
