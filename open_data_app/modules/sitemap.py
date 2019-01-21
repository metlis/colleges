from django.contrib.sitemaps import Sitemap

from open_data_app.models import Degree, Carnegie, Religion, Level, Ownership, Locale
from open_data_app.models.college import College
from open_data_app.models.state import State
from open_data_app.models.region import Region
from django.urls import reverse
from django.utils.text import slugify
import re

params_verbose = {
    'ownership': {
        'values': Ownership.objects.all().values('id'),
        'verbose': 'ownership'
    },
    'locale': {
        'values': Locale.objects.all().values('id'),
        'verbose': 'locale'
    },
    'highest_grad_degree': {
        'values': Degree.objects.all().values('id'),
        'verbose': 'degree'
    },
    'carnegie_basic': {
        'values': Carnegie.objects.all().values('id'),
        'verbose': 'carnegie'
    },
    'religous': {
        'values': Religion.objects.all().values('id'),
        'verbose': 'religion'
    },
    'inst_level': {
        'values': Level.objects.all().values('id'),
        'verbose': 'level'
    },
    'hist_black': {
        'values': [0, 1],
        'verbose': 'hist_black'
    },
    'predom_black': {
        'values': [0, 1],
        'verbose': 'predom_black'
    },
    'men_only': {
        'values': [0, 1],
        'verbose': 'men_only'
    },
    'women_only': {
        'values': [0, 1],
        'verbose': 'women_only'
    },
    'online_only': {
        'values': [0, 1],
        'verbose': 'online_only'
    },
    'cur_operating': {
        'values': [0, 1],
        'verbose': 'cur_operating'
    },
}
colleges = College.objects.all()
regions = Region.objects.all()
states = State.objects.all()

class CollegesSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return colleges


class StatesSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return states


class RegionsSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return regions


class DisciplinesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['agriculture', 'architecture', 'ethnic_cultural_gender', 'biological', 'business_marketing',
                'communication', 'communications_technology', 'computer', 'construction', 'education',
                'engineering', 'engineering_technology', 'english', 'family_consumer_science', 'language',
                'health', 'history', 'security_law_enforcement', 'legal', 'humanities', 'library', 'mathematics',
                'mechanic_repair_technology', 'military', 'multidiscipline', 'resources',
                'parks_recreation_fitness', 'personal_culinary', 'philosophy_religious', 'physical_science',
                'precision_production', 'psychology', 'public_administration_social_service',
                'science_technology', 'social_science', 'theology_religious_vocation', 'transportation',
                'visual_performing']

    def location(self, item):
        return reverse('college_app:filter_no_values', kwargs={
            'param': item,
        }
                       )


class FilterParamsSitemap(Sitemap):
    protocol = 'https'

    def location(self, item):
        return reverse('college_app:filter_values', kwargs={
            'param': item['param'],
            'param_value': item['param_value'],
        }
                       )

    def items(self):
        params = {
            'ownership': Ownership.objects.all().values('id'),
            'locale': Locale.objects.all().values('id'),
            'degree': Degree.objects.all().values('id'),
            'carnegie': Carnegie.objects.all().values('id'),
            'religion': Religion.objects.all().values('id'),
            'level': Level.objects.all().values('id'),
            'hist_black': [0, 1],
            'predom_black': [0, 1],
            'men_only': [0, 1],
            'women_only': [0, 1],
            'online_only': [0, 1],
            'cur_operating': [0, 1],
        }

        values = []
        for param in params:
            for i in params[param]:
                try:
                    value = i['id']
                except:
                    value = i
                values.append({
                    'param': param,
                    'param_value': value
                })

        return values


class StateFilterParamsSitemap(Sitemap):
    protocol = 'https'
    def items(self):
        values = []
        for state in states:
            state_slug = slugify(state.name)
            state_id = state.id
            for param in params_verbose:
                for i in params_verbose[param]['values']:
                    try:
                        value = i['id']
                    except:
                        value = i
                    filtered_colleges = colleges.filter(state__id=state_id).filter(**{param: value})
                    if len(filtered_colleges) > 0:
                        values.append({
                            'param': params_verbose[param]['verbose'],
                            'param_value': value,
                            'state_slug': state_slug,
                            'state_id': state_id,
                        })

        return values

    def location(self, item):
        return reverse('college_app:state_param', kwargs={
            'param': item['param'],
            'param_value': item['param_value'],
            'state_slug': item['state_slug'],
            'state_id': item['state_id'],
        }
                       )

class RegionFilterParamsSitemap(Sitemap):
    protocol = 'https'
    def items(self):
        values = []
        for region in regions:
            region_id = region.id
            try:
                region_re = re.search('(.*?)\s\((.*?)\)', region.name)
                region_name = region_re.group(1)
                region_slug = slugify(region_name)

                for param in params_verbose:
                    for i in params_verbose[param]['values']:
                        try:
                            value = i['id']
                        except:
                            value = i
                        filtered_colleges = colleges.filter(region__id=region_id).filter(**{param: value})
                        if len(filtered_colleges) > 0:
                            values.append({
                                'param': params_verbose[param]['verbose'],
                                'param_value': value,
                                'region_slug': region_slug,
                                'region_id': region_id,
                            })
            except:
                pass

        return values

    def location(self, item):
        return reverse('college_app:region_param', kwargs={
            'param': item['param'],
            'param_value': item['param_value'],
            'region_slug': item['region_slug'],
            'region_id': item['region_id'],
        }
                       )