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

        disciplines = ['agriculture', 'architecture', 'ethnic_cultural_gender', 'biological', 'business_marketing',
                       'communication', 'communications_technology', 'computer', 'construction', 'education',
                       'engineering', 'engineering_technology', 'english', 'family_consumer_science', 'language',
                       'health', 'history', 'security_law_enforcement', 'legal', 'humanities', 'library', 'mathematics',
                       'mechanic_repair_technology', 'military', 'multidiscipline', 'resources',
                       'parks_recreation_fitness', 'personal_culinary', 'philosophy_religious', 'physical_science',
                       'precision_production', 'psychology', 'public_administration_social_service',
                       'science_technology', 'social_science', 'theology_religious_vocation', 'transportation',
                       'visual_performing']

        disciplines_vals = []

        for disc in disciplines:
            val = getattr(college, disc)
            if float(val) > 0:
                val_formatted = float("{0:.2f}".format(val * 100))
                disciplines_vals.append([disc, val_formatted])

        disciplines_vals_sorted = sorted(disciplines_vals, key=lambda x: x[1], reverse=True)

        if college_slug != slugify(college.name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return render(request, 'college.html', {'college': college,
                                                    'college_id': college_id,
                                                    'college_slug': college_slug,
                                                    'top_disciplines': disciplines_vals_sorted[:5],
                                                    })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
