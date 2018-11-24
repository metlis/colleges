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

    # academics section
    agriculture = models.FloatField(null=True, verbose_name='agriculture')
    architecture = models.FloatField(null=True, verbose_name='architecture')
    ethnic_cultural_gender = models.FloatField(null=True, verbose_name='ethnic_cultural_gender')
    biological = models.FloatField(null=True, verbose_name='biological')
    business_marketing = models.FloatField(null=True, verbose_name='business_marketing')
    communication = models.FloatField(null=True, verbose_name='communication')
    communications_technology = models.FloatField(null=True, verbose_name='communications_technology')
    computer = models.FloatField(null=True, verbose_name='computer')
    construction = models.FloatField(null=True, verbose_name='construction')
    education = models.FloatField(null=True, verbose_name='education')
    engineering = models.FloatField(null=True, verbose_name='engineering')
    engineering_technology = models.FloatField(null=True, verbose_name='engineering_technology')
    english = models.FloatField(null=True, verbose_name='english')
    family_consumer_science = models.FloatField(null=True, verbose_name='family_consumer_science')
    language = models.FloatField(null=True, verbose_name='language')
    health = models.FloatField(null=True, verbose_name='health')
    history = models.FloatField(null=True, verbose_name='history')
    security_law_enforcement = models.FloatField(null=True, verbose_name='security_law_enforcement')
    legal = models.FloatField(null=True, verbose_name='legal')
    humanities = models.FloatField(null=True, verbose_name='humanities')
    library = models.FloatField(null=True, verbose_name='library')
    mathematics = models.FloatField(null=True, verbose_name='mathematics')
    mechanic_repair_technology = models.FloatField(null=True, verbose_name='mechanic_repair_technology')
    military = models.FloatField(null=True, verbose_name='military')
    multidiscipline = models.FloatField(null=True, verbose_name='multidiscipline')
    resources = models.FloatField(null=True, verbose_name='resources')
    parks_recreation_fitness = models.FloatField(null=True, verbose_name='parks_recreation_fitness')
    personal_culinary = models.FloatField(null=True, verbose_name='personal_culinary')
    philosophy_religious = models.FloatField(null=True, verbose_name='philosophy_religious')
    physical_science = models.FloatField(null=True, verbose_name='physical_science')
    precision_production = models.FloatField(null=True, verbose_name='precision_production')
    psychology = models.FloatField(null=True, verbose_name='psychology')
    public_administration_social_service = models.FloatField(null=True, verbose_name='public_administration_social_service')
    science_technology = models.FloatField(null=True, verbose_name='science_technology')
    social_science = models.FloatField(null=True, verbose_name='social_science')
    theology_religious_vocation = models.FloatField(null=True, verbose_name='theology_religious_vocation')
    transportation = models.FloatField(null=True, verbose_name='transportation')
    visual_performing = models.FloatField(null=True, verbose_name='visual_performing')


    full_data = models.TextField()

    def __str__(self):
        return self.name

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

                    # school section
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


                    # academics section
                    college.agriculture = check_val(col_values[61], False)
                    college.architecture = check_val(col_values[63], False)
                    college.ethnic_cultural_gender = check_val(col_values[64], False)
                    college.biological = check_val(col_values[78], False)
                    college.business_marketing = check_val(col_values[97], False)
                    college.communication = check_val(col_values[65], False)
                    college.communications_technology = check_val(col_values[66], False)
                    college.computer = check_val(col_values[67], False)
                    college.construction = check_val(col_values[91], False)
                    college.education = check_val(col_values[69], False)
                    college.engineering = check_val(col_values[70], False)
                    college.engineering_technology = check_val(col_values[71], False)
                    college.english = check_val(col_values[75], False)
                    college.family_consumer_science = check_val(col_values[73], False)
                    college.language = check_val(col_values[72], False)
                    college.health = check_val(col_values[96], False)
                    college.history = check_val(col_values[98], False)
                    college.security_law_enforcement = check_val(col_values[88], False)
                    college.legal = check_val(col_values[74], False)
                    college.humanities = check_val(col_values[76], False)
                    college.library = check_val(col_values[77], False)
                    college.mathematics = check_val(col_values[79], False)
                    college.mechanic_repair_technology = check_val(col_values[92], False)
                    college.military = check_val(col_values[80], False)
                    college.multidiscipline = check_val(col_values[81], False)
                    college.resources = check_val(col_values[62], False)
                    college.parks_recreation_fitness = check_val(col_values[82], False)
                    college.personal_culinary = check_val(col_values[68], False)
                    college.philosophy_religious = check_val(col_values[83], False)
                    college.physical_science = check_val(col_values[85], False)
                    college.precision_production = check_val(col_values[93], False)
                    college.psychology = check_val(col_values[87], False)
                    college.public_administration_social_service = check_val(col_values[89], False)
                    college.science_technology = check_val(col_values[86], False)
                    college.social_science = check_val(col_values[90], False)
                    college.theology_religious_vocation = check_val(col_values[84], False)
                    college.transportation = check_val(col_values[94], False)
                    college.visual_performing = check_val(col_values[95], False)


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
        # items for the second level of filtration + region or state
        if init_filter and entity:
            filters = {entity: entity_id,
                       init_filter: init_filter_val,
                       }

            colleges = cls.objects.filter(**filters)
            # third level filters
            if filters_set:
                colleges = colleges.filter(**filters_set)
        # items for the second level of filtration without region or state
        elif init_filter:
            filters = {init_filter: init_filter_val,}

            colleges = cls.objects.filter(**filters)
            # third level filters
            if filters_set:
                colleges = colleges.filter(**filters_set)
        # region or state
        elif entity:
            colleges = cls.objects.filter(**{entity: entity_id})
        # third level filters
        elif filters_set:
            colleges = cls.objects.filter(**filters_set)
        else:
            colleges = cls.objects.all()

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
        """
        Searches field by verbose name and takes its value. Works for any filter page

        :param entity: state or region
        :param entity_id:
        :param param: verbose name of a field
        :param param_value: value of a field
        :return:
        """
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
                elif param in ['city', 'city_slug']:
                    if entity == 'state':
                        query_field = cls.objects.filter(state__id=entity_id).filter(
                            **{'city_slug': param_value}).values(
                            'city').distinct()
                    elif entity == 'region':
                        query_field = cls.objects.filter(region__id=entity_id).filter(
                            **{'city_slug': param_value}).values(
                            'city').distinct()
                    else:
                        query_field = cls.objects.filter(**{'city_slug': param_value}).values('city').distinct()
                    if len(query_field) > 0:
                        query_val = query_field[0]['city']
                        return param, query_val, param, query_val
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
                # yes/no queries
                else:
                    dict = cls.get_dict()

                    query_val = dict[param][int(param_value)]

                return param, query_val, field._verbose_name, param_value
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
