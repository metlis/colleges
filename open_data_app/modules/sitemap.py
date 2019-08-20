import re
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.text import slugify

from open_data_app.models import Degree, Carnegie, Religion, Level, Ownership, Locale
from open_data_app.models.college import College
from open_data_app.models.state import State
from open_data_app.models.region import Region
from open_data_app.models.dictionary import Dictionary

PARAMS = {
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
COLLEGES = College.objects.all()
REGIONS = Region.objects.all()
STATES = State.objects.all()


class CollegesSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return COLLEGES


class StatesSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return STATES


class RegionsSitemap(Sitemap):
    protocol = 'https'

    def location(self, obj):
        return obj.get_absolute_path()

    def items(self):
        return REGIONS


class DisciplinesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        try:
            content = Dictionary.objects.get(name='discipline_slugs').content
            if content is not None:
                return content
            else:
                return []
        except ObjectDoesNotExist:
            return []

    def location(self, item):
        return reverse('college_app:filter_no_values', kwargs={
            'param_name': item,
        }
                       )


class FilterParamsSitemap(Sitemap):
    protocol = 'https'

    def location(self, item):
        return reverse('college_app:filter_values', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
        }
                       )

    def items(self):
        param_values = []

        for param_name in PARAMS:
            for i in PARAMS[param_name]:
                try:
                    param_value = i['id']
                except TypeError:
                    param_value = i
                param_values.append({
                    'param_name': param_name,
                    'param_value': param_value
                })

        return param_values


class StateFilterParamsSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        param_values = []

        for state in STATES:
            state_slug = slugify(state.name)
            state_id = state.id

            for param_name in PARAMS:
                for i in PARAMS[param_name]:
                    try:
                        param_value = i['id']
                    except TypeError:
                        param_value = i
                    filtered_colleges = COLLEGES.filter(state__id=state_id).filter(**{param_name: param_value})
                    if len(filtered_colleges) > 0:
                        param_values.append({
                            'param_name': param_name,
                            'param_value': param_value,
                            'state_slug': state_slug,
                            'state_id': state_id,
                        })

        return param_values

    def location(self, item):
        return reverse('college_app:state_param', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
            'state_slug': item['state_slug'],
            'state_id': item['state_id'],
        }
                       )


class RegionFilterParamsSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        param_values = []

        for region in REGIONS:
            region_id = region.id

            try:
                region_re = re.search('(.*?)\s\((.*?)\)', region.name)
                region_name = region_re.group(1)
                region_slug = slugify(region_name)

                for param_name in PARAMS:
                    for i in PARAMS[param_name]:
                        try:
                            param_value = i['id']
                        except TypeError:
                            param_value = i
                        filtered_colleges = COLLEGES.filter(region__id=region_id).filter(**{param_name: param_value})
                        if len(filtered_colleges) > 0:
                            param_values.append({
                                'param_name': param_name,
                                'param_value': param_value,
                                'region_slug': region_slug,
                                'region_id': region_id,
                            })
            except:
                pass

        return param_values

    def location(self, item):
        return reverse('college_app:region_param', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
            'region_slug': item['region_slug'],
            'region_id': item['region_id'],
        }
                       )
