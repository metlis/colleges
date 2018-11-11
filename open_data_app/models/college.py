from django.db import models
import csv
import os
import sys
import urllib.parse

from django.http import HttpResponseNotFound

from settings import *
from django.utils.text import slugify
from open_data_app.models.state import State
from open_data_app.models.region import Region
from open_data_app.models.ownership import Ownership
from open_data_app.models.locale import Locale
from open_data_app.models.degree import Degree
from open_data_app.models.carnegie import Carnegie
from open_data_app.models.religion import Religion
from open_data_app.models.level import Level


class College(models.Model):
    # school section
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    city_slug = models.SlugField(max_length=255, blank=True, verbose_name='city')
    zip = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, verbose_name='state')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True)
    ownership = models.ForeignKey(Ownership, on_delete=models.PROTECT, null=True, verbose_name='ownership')
    locale = models.ForeignKey(Locale, on_delete=models.PROTECT, null=True, verbose_name='locale')
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    highest_grad_degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True, verbose_name='degree')
    carnegie_basic = models.ForeignKey(Carnegie, on_delete=models.PROTECT, null=True, verbose_name='carnegie')
    hist_black = models.IntegerField(null=True, verbose_name='hist_black')
    predom_black = models.IntegerField(null=True, verbose_name='predom_black')
    hispanic = models.IntegerField(null=True, verbose_name='hispanic')
    men_only = models.IntegerField(null=True, verbose_name='men_only')
    women_only = models.IntegerField(null=True, verbose_name='women_only')
    religous = models.ForeignKey(Religion, on_delete=models.PROTECT, null=True, verbose_name='religion')
    online_only = models.IntegerField(null=True, verbose_name='online_only')
    inst_level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, verbose_name='level')
    cur_operating = models.IntegerField(null=True, verbose_name='cur_operating')

    full_data = models.TextField()

    @classmethod
    def parse_csv(cls):
        csv.field_size_limit(sys.maxsize)
        with open(os.path.abspath(os.path.join(BASE_DIR, 'open_data_app', 'static/data.csv')), 'r', newline='',
                  encoding='utf-8') as file:

            colleges = []
            row_num = 1
            for row in file:
                if row_num > 1:
                    col_values = row.split(',')

                    if len(col_values) != 1847:

                        links = []
                        i = row.index('"') + 1
                        inext = row.index('"', i)
                        links.append(row[i:inext])

                        row = row.split('"')

                        for i, e in enumerate(row):
                            if e in links:
                                row[i] = urllib.parse.quote_plus(e)

                        row = ''.join(row)
                        col_values = row.split(',')

                    def check_val(val, str):
                        if val == 'NULL' and not str:
                            return None
                        elif val == 'NULL' and str:
                            return ''
                        else:
                            return val

                    def get_instance(arr):
                        try:
                            return arr[0]
                        except:
                            pass

                    college = cls()
                    college.id = col_values[0]
                    college.name = col_values[3]
                    college.slug = slugify(col_values[3])
                    college.city = col_values[4]
                    college.city_slug = slugify(col_values[4])
                    college.zip = col_values[6]

                    state = get_instance(State.objects.filter(id=check_val(col_values[17], False)))
                    college.state = state

                    region = get_instance(Region.objects.filter(id=check_val(col_values[18], False)))
                    college.region = region

                    ownership = get_instance(Ownership.objects.filter(id=check_val(col_values[16], False)))
                    college.ownership = ownership

                    locale = get_instance(Locale.objects.filter(id=check_val(col_values[19], False)))
                    college.locale = locale

                    college.latitude = check_val(col_values[21], False)
                    college.longitude = check_val(col_values[22], False)

                    degree = get_instance(Degree.objects.filter(id=check_val(col_values[15], False)))
                    college.highest_grad_degree = degree

                    carnegie_basic = get_instance(Carnegie.objects.filter(code_num=check_val(col_values[23], False)))
                    college.carnegie_basic = carnegie_basic

                    college.hist_black = check_val(col_values[26], False)
                    college.predom_black = check_val(col_values[27], False)
                    college.hispanic = check_val(col_values[31], False)
                    college.men_only = check_val(col_values[33], False)
                    college.women_only = check_val(col_values[34], False)

                    religion = get_instance(Religion.objects.filter(code_num=check_val(col_values[35], False)))
                    college.religous = religion

                    college.online_only = check_val(col_values[289], False)

                    level = get_instance(Level.objects.filter(id=check_val(col_values[1738], False)))
                    college.inst_level = level

                    college.cur_operating = check_val(col_values[315], False)
                    college.url = check_val(col_values[8], True)
                    college.full_data = ','.join(col_values)

                    colleges.append(college)
                row_num += 1

            cls.objects.bulk_create(colleges)

    @classmethod
    def get_dict(cls):
        dict = {'hist_black': ['Historically not black', 'Historically black'],
                'predom_black': ['Predominantely not black', 'Predominantely black'],
                'hispanic': ['Predominantely not hispanic', 'Predominantely hispanic'],
                'men_only': ['Not men-only', 'Men-only'],
                'women_only': ['Not women-only', 'Women-only'],
                'online_only': ['Not online-only', 'Online-only'],
                'cur_operating': ['Currently closed', 'Currently operating'],
                }
        return dict

    @classmethod
    def get_filters(cls, entity, entity_id, excluded_filters='', get_filter='', init_filter='', init_filter_val='',
                    filters_set=''):
        """

        :param entity: state or region for initial level of filtration
        :param entity_id: state_id or region_id
        :param excluded_filters: filters that should not be returned
        :param get_filter: specific filter's name to return
        :param init_filter: second level filtration
        :param init_filter_val: second level filtration value
        :param filters_set: third level filtration value
        :return:
        """
        # items for the second level of filtration
        if init_filter:
            filters = {entity: entity_id,
                       init_filter: init_filter_val,
                       }

            colleges = cls.objects.filter(**filters)
            # third level filters
            if filters_set:
                colleges = colleges.filter(**filters_set)
        # items for initial level of filtration
        else:
            colleges = cls.objects.filter(**{entity: entity_id})

        colleges_cities = colleges.values_list('city',
                                               'city_slug').order_by('city').exclude(city=None).distinct()
        colleges_states = colleges.values_list('state__id',
                                               'state__name').order_by('state__name').exclude(
            state__name=None).distinct()
        colleges_ownership = colleges.values_list('ownership__id',
                                                  'ownership__description').order_by('ownership__id').exclude(
            ownership__description=None).exclude(
            ownership__description='Not applicable').distinct()
        colleges_locales = colleges.values_list('locale__id',
                                                'locale__description').order_by('locale__id').exclude(
            locale__description=None).exclude(
            locale__description='Not applicable').distinct()
        colleges_degrees = colleges.values_list('highest_grad_degree__id',
                                                'highest_grad_degree__description').order_by(
            'highest_grad_degree__id').exclude(highest_grad_degree__description=None).exclude(
            highest_grad_degree__description='Not applicable').distinct()
        colleges_carnegie_basic = colleges.values_list('carnegie_basic__id',
                                                       'carnegie_basic__description').order_by(
            'carnegie_basic__description').exclude(carnegie_basic__description=None).exclude(
            carnegie_basic__description='Not applicable').distinct()
        colleges_religions = colleges.values_list('religous__id',
                                                  'religous__name').order_by(
            'religous__name').exclude(religous__name=None).distinct()
        colleges_levels = colleges.values_list('inst_level__id',
                                               'inst_level__description').order_by('inst_level__id').distinct()
        colleges_hist_black = colleges.values('hist_black').exclude(hist_black=None).distinct()
        colleges_predom_black = colleges.values('predom_black').exclude(predom_black=None).distinct()
        colleges_hispanic = colleges.values('hispanic').exclude(hispanic=None).distinct()
        colleges_men_only = colleges.values('men_only').exclude(men_only=None).distinct()
        colleges_women_only = colleges.values('women_only').exclude(women_only=None).distinct()
        colleges_online_only = colleges.values('online_only').exclude(online_only=None).distinct()
        colleges_cur_operating = colleges.values('cur_operating').exclude(cur_operating=None).distinct()

        filters = {'city': colleges_cities,
                   'state': colleges_states,
                   'ownership': colleges_ownership,
                   'locale': colleges_locales,
                   'highest_grad_degree': colleges_degrees,
                   'carnegie_basic': colleges_carnegie_basic,
                   'religous': colleges_religions,
                   'inst_level': colleges_levels,
                   'hist_black': colleges_hist_black,
                   'predom_black': colleges_predom_black,
                   'hispanic': colleges_hispanic,
                   'men_only': colleges_men_only,
                   'women_only': colleges_women_only,
                   'online_only': colleges_online_only,
                   'cur_operating': colleges_cur_operating, }

        if len(excluded_filters) > 0:
            for i in excluded_filters:
                try:
                    filters[i] = []
                except:
                    pass

        if len(get_filter) > 0:
            for i in filters:
                if i == get_filter:
                    return filters[i]

        return filters

    @classmethod
    def get_filter_val(cls, entity, entity_id, param, param_value):
        college_fields = cls._meta.get_fields()

        for field in college_fields:
            if param == field._verbose_name or param == field.name:

                # if verbose name and name are different, change query param to name of the field
                if param != field.attname:
                    param = field.attname

                # for relational fields get related object
                if field.related_model is not None:
                    rel_obj_exists = field.related_model.objects.filter(pk=param_value).exists()

                    if rel_obj_exists:
                        rel_obj = field.related_model.objects.get(pk=param_value)

                        # get relational field text value
                        try:
                            query_val = rel_obj.description
                        except:
                            query_val = rel_obj.name

                # for non-relational fields (city) get query value
                elif param in ['city_slug']:
                    if entity == 'state':
                        query_field = cls.objects.filter(state__id=entity_id).filter(**{param: param_value}).values(
                        field._verbose_name).distinct()
                    else:
                        query_field = cls.objects.filter(region__id=entity_id).filter(**{param: param_value}).values(
                            field._verbose_name).distinct()
                    if len(query_field) > 0:
                        query_val = query_field[0][field._verbose_name]
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
                # yes/no queries
                else:
                    dict = cls.get_dict()

                    query_val = dict[param][int(param_value)]

                return param, query_val