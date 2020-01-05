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
from open_data_app.models.rating import Rating
from open_data_app.models.page import Page

PARAMS = {
    'ownership__slug': Ownership.objects.all().values('slug'),
    'locale__slug': Locale.objects.all().values('slug'),
    'degree__slug': Degree.objects.all().values('slug'),
    'carnegie__slug': Carnegie.objects.all().values('slug'),
    'religion__slug': Religion.objects.all().values('slug'),
    'level__slug': Level.objects.all().values('slug'),
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
CITIES = College.objects.values('city_slug').distinct()
RATINGS = Rating.objects.all().values('url')
PAGES = Page.objects.all().exclude(rating__isnull=False).values('url')


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


class CitiesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        cities = []

        for city in CITIES:
            cities.append(city['city_slug'])

        return cities

    def location(self, item):
        return reverse('college_app:filter_values', kwargs={
            'param_name': 'city_slug',
            'param_value': item,
        })


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
        })


class FilterParamsSitemap(Sitemap):
    protocol = 'https'

    def location(self, item):
        return reverse('college_app:filter_values', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
        })

    def items(self):
        param_values = []

        for param_name in PARAMS:
            for i in PARAMS[param_name]:
                try:
                    param_value = i['slug']
                except TypeError:
                    param_value = i
                param_values.append({
                    'param_name': param_name.replace('__slug', ''),
                    'param_value': param_value
                })

        return param_values


class StateFilterParamsSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        param_values = []

        for state in STATES:
            state_slug = slugify(state.name)

            for param_name in PARAMS:
                for i in PARAMS[param_name]:
                    try:
                        param_value = i['slug']
                    except TypeError:
                        param_value = i
                    filtered_colleges = COLLEGES.filter(state__slug=state_slug).filter(**{param_name: param_value})
                    if len(filtered_colleges) > 0:
                        param_values.append({
                            'param_name': param_name.replace('__slug', ''),
                            'param_value': param_value,
                            'state_slug': state_slug,
                        })

        return param_values

    def location(self, item):
        return reverse('college_app:geo_param', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
            'geo_slug': item['state_slug'],
            'geo_name': 'state',
        })


class RegionFilterParamsSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        param_values = []

        for region in REGIONS:

            try:
                region_re = re.search('(.*?)\s\((.*?)\)', region.name)
                region_name = region_re.group(1)
                region_slug = slugify(region_name)

                for param_name in PARAMS:
                    for i in PARAMS[param_name]:
                        try:
                            param_value = i['slug']
                        except TypeError:
                            param_value = i
                        filtered_colleges = COLLEGES.filter(region__slug=region_slug).filter(**{param_name: param_value})
                        if len(filtered_colleges) > 0:
                            param_values.append({
                                'param_name': param_name.replace('__slug', ''),
                                'param_value': param_value,
                                'region_slug': region_slug,
                            })
            except:
                pass

        return param_values

    def location(self, item):
        return reverse('college_app:geo_param', kwargs={
            'param_name': item['param_name'],
            'param_value': item['param_value'],
            'geo_slug': item['region_slug'],
            'geo_name': 'region',
        })


class RatingsSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        urls = []

        for rating in RATINGS:
            urls.append(rating['url'])

        return urls

    def location(self, item):
        return reverse('college_app:create_rating', kwargs={'rating_url': item,})


class PagesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        urls = []

        for page in PAGES:
            urls.append(page['url'])

        return urls

    def location(self, item):
        return reverse('college_app:show_content_page', kwargs={'page_url': item,})