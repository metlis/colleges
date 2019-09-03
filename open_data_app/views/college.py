from django.shortcuts import render
from django.utils.text import slugify
from django.http import Http404
from django.urls import reverse
from settings import *

from open_data_app.models import College, Carnegie, Degree, Level, Locale, Ownership, Religion, Region, State


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
                        disciplines_vals.append([dictionary[d], val_formatted,
                                                reverse('college_app:filter_no_values', kwargs={'param_name': d})])
                except:
                    pass

            top_disciplines = sorted(disciplines_vals, key=lambda x: x[1], reverse=True)

            # referring page's url for the back button
            referer = request.META.get('HTTP_REFERER')

            # college's categories tags
            tags = []

            try:
                region = Region.objects.get(id=college.region_id)
                tags.append([region.name, reverse('college_app:region', kwargs={'region_slug': region.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                state = State.objects.get(id=college.state_id)
                tags.append([state.name, reverse('college_app:state', kwargs={'state_slug': state.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                carnegie = Carnegie.objects.get(id=college.carnegie_id)
                tags.append([carnegie.description, reverse('college_app:filter_values',
                                                           kwargs={'param_name': 'carnegie',
                                                                   'param_value': carnegie.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                degree = Degree.objects.get(id=college.degree_id)
                tags.append([degree.description, reverse('college_app:filter_values',
                                                         kwargs={'param_name': 'degree',
                                                                 'param_value': degree.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                level = Level.objects.get(id=college.level_id)
                tags.append([level.description, reverse('college_app:filter_values',
                                                        kwargs={'param_name': 'level',
                                                                'param_value': level.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                locale = Locale.objects.get(id=college.locale_id)
                tags.append([locale.description, reverse('college_app:filter_values',
                                                         kwargs={'param_name': 'locale',
                                                                 'param_value': locale.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                ownership = Ownership.objects.get(id=college.ownership_id)
                tags.append([ownership.description, reverse('college_app:filter_values',
                                                            kwargs={'param_name': 'ownership',
                                                                    'param_value': ownership.slug})])
            except Exception as e:
                print(e)
                pass

            try:
                religion = Religion.objects.get(id=college.religion_id)
                tags.append([religion.description, reverse('college_app:filter_values',
                                                           kwargs={'param_name': 'religion',
                                                                   'param_value': religion.slug})])
            except Exception as e:
                print(e)
                pass

            return render(request, 'college.html', {'college': college,
                                                    'top_disciplines': top_disciplines[:5],
                                                    'college_disciplines': disciplines_vals,
                                                    'is_favourite': is_favourite,
                                                    'maps_key': GOOGLE_MAPS_API,
                                                    'referer': referer,
                                                    'tags': tags,
                                                    })
    else:
        raise Http404()
