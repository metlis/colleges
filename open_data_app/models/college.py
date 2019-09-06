import csv
import sys
import urllib.parse

from settings import *
from django.db import models
from django.db.models import Avg, Max, Min, F
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

from open_data_app.models.state import State
from open_data_app.models.region import Region
from open_data_app.models.ownership import Ownership
from open_data_app.models.locale import Locale
from open_data_app.models.degree import Degree
from open_data_app.models.carnegie import Carnegie
from open_data_app.models.religion import Religion
from open_data_app.models.level import Level
from open_data_app.models.dictionary import Dictionary


class College(models.Model):
    # school section
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    city_slug = models.SlugField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    calc_url = models.CharField(max_length=255, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True)
    ownership = models.ForeignKey(Ownership, on_delete=models.PROTECT, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.PROTECT, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    carnegie = models.ForeignKey(Carnegie, on_delete=models.PROTECT, null=True)
    hist_black = models.IntegerField(null=True)
    predom_black = models.IntegerField(null=True)
    hispanic = models.IntegerField(null=True)
    men_only = models.IntegerField(null=True)
    women_only = models.IntegerField(null=True)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT, null=True)
    online_only = models.IntegerField(null=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True)
    cur_operating = models.IntegerField(null=True)

    # academics section
    agriculture = models.FloatField(null=True)
    architecture = models.FloatField(null=True)
    ethnic_cultural_gender = models.FloatField(null=True)
    biological = models.FloatField(null=True)
    business_marketing = models.FloatField(null=True)
    communication = models.FloatField(null=True)
    communications_technology = models.FloatField(null=True)
    computer = models.FloatField(null=True)
    construction = models.FloatField(null=True)
    education = models.FloatField(null=True)
    engineering = models.FloatField(null=True)
    engineering_technology = models.FloatField(null=True)
    english = models.FloatField(null=True)
    family_consumer_science = models.FloatField(null=True)
    language = models.FloatField(null=True)
    health = models.FloatField(null=True)
    history = models.FloatField(null=True)
    security_law_enforcement = models.FloatField(null=True)
    legal = models.FloatField(null=True)
    humanities = models.FloatField(null=True)
    library = models.FloatField(null=True)
    mathematics = models.FloatField(null=True)
    mechanic_repair_technology = models.FloatField(null=True)
    military = models.FloatField(null=True)
    multidiscipline = models.FloatField(null=True)
    resources = models.FloatField(null=True)
    parks_recreation_fitness = models.FloatField(null=True)
    personal_culinary = models.FloatField(null=True)
    philosophy_religious = models.FloatField(null=True)
    physical_science = models.FloatField(null=True)
    precision_production = models.FloatField(null=True)
    psychology = models.FloatField(null=True)
    public_administration_social_service = models.FloatField(null=True)
    science_technology = models.FloatField(null=True)
    social_science = models.FloatField(null=True)
    theology_religious_vocation = models.FloatField(null=True)
    transportation = models.FloatField(null=True)
    visual_performing = models.FloatField(null=True)

    # cost
    average_net_price_public = models.FloatField(null=True)
    average_net_price_private = models.FloatField(null=True)
    average_cost_of_attendance_academic = models.FloatField(null=True)
    average_cost_of_attendance_program = models.FloatField(null=True)
    in_state_tuition = models.FloatField(null=True)
    out_state_tuition = models.FloatField(null=True)
    average_net_price_pub_30 = models.FloatField(null=True)
    average_net_price_pub_48 = models.FloatField(null=True)
    average_net_price_pub_75 = models.FloatField(null=True)
    average_net_price_pub_110 = models.FloatField(null=True)
    average_net_price_pub_110_plus = models.FloatField(null=True)
    average_net_price_priv_30 = models.FloatField(null=True)
    average_net_price_priv_48 = models.FloatField(null=True)
    average_net_price_priv_75 = models.FloatField(null=True)
    average_net_price_priv_110 = models.FloatField(null=True)
    average_net_price_priv_110_plus = models.FloatField(null=True)

    # aid
    pell_grand = models.FloatField(null=True)
    federal_loan = models.FloatField(null=True)
    debt_completed = models.FloatField(null=True)
    debt_not_completed = models.FloatField(null=True)
    debt_completed_median = models.FloatField(null=True)
    monthly_payments = models.FloatField(null=True)

    # completion
    completion_rate_four_year = models.FloatField(null=True)
    completion_rate_less_four_year = models.FloatField(null=True)
    completion_rate_four_year_pooled = models.FloatField(null=True)
    completion_rate_less_four_year_pooled = models.FloatField(null=True)
    retention_rate_four_year_pooled = models.FloatField(null=True)
    retention_rate_less_four_year_pooled = models.FloatField(null=True)

    # earnings
    mean_earnings = models.FloatField(null=True)
    median_earnings = models.FloatField(null=True)

    # student
    undergrad_students = models.FloatField(null=True)
    students_white = models.FloatField(null=True)
    students_black = models.FloatField(null=True)
    students_hispanic = models.FloatField(null=True)
    students_asian = models.FloatField(null=True)
    students_native = models.FloatField(null=True)
    students_pacific = models.FloatField(null=True)
    students_multiple_races = models.FloatField(null=True)
    students_non_resident = models.FloatField(null=True)
    students_unknown_race = models.FloatField(null=True)
    students_part_time = models.FloatField(null=True)
    students_female = models.FloatField(null=True)
    students_family_income = models.FloatField(null=True)

    # admission
    admission_rate = models.FloatField(null=True)
    sat_reading = models.FloatField(null=True)
    sat_math = models.FloatField(null=True)
    sat_writing = models.FloatField(null=True)
    sat_average = models.FloatField(null=True)
    act_cumulative = models.FloatField(null=True)
    act_english = models.FloatField(null=True)
    act_math = models.FloatField(null=True)
    act_writing = models.FloatField(null=True)

    def __str__(self):
        return self.name

    @classmethod
    def parse_csv(cls):
        csv.field_size_limit(sys.maxsize)
        with open(os.path.abspath(os.path.join(BASE_DIR, 'open_data_app', DATA_PATH)), 'r', newline='',
                  encoding='utf-8') as file:

            colleges = []
            row_num = 1
            for row in file:

                if row_num > 1:
                    col_values = row.split(',')

                    if len(col_values) != 1977:

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
                        if (val == 'NULL' or val == 'NU' or val == 'PrivacySuppressed') and not str:
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
                    college.degree = degree

                    carnegie = get_instance(Carnegie.objects.filter(code_num=check_val(col_values[23], False)))
                    college.carnegie = carnegie

                    college.hist_black = check_val(col_values[26], False)
                    college.predom_black = check_val(col_values[27], False)
                    college.hispanic = check_val(col_values[31], False)
                    college.men_only = check_val(col_values[33], False)
                    college.women_only = check_val(col_values[34], False)

                    religion = get_instance(Religion.objects.filter(code_num=check_val(col_values[35], False)))
                    college.religion = religion

                    college.online_only = check_val(col_values[289], False)

                    level = get_instance(Level.objects.filter(id=check_val(col_values[1738], False)))
                    college.level = level

                    college.cur_operating = check_val(col_values[315], False)
                    college.url = check_val(col_values[8], True)
                    college.calc_url = check_val(col_values[9], True)

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

                    # cost
                    college.average_net_price_public = check_val(col_values[316], False)
                    college.average_net_price_private = check_val(col_values[317], False)
                    college.average_cost_of_attendance_academic = check_val(col_values[376], False)
                    college.average_cost_of_attendance_program = check_val(col_values[377], False)
                    college.in_state_tuition = check_val(col_values[378], False)
                    college.out_state_tuition = check_val(col_values[379], False)
                    college.average_net_price_pub_30 = check_val(col_values[320], False)
                    college.average_net_price_pub_48 = check_val(col_values[321], False)
                    college.average_net_price_pub_75 = check_val(col_values[322], False)
                    college.average_net_price_pub_110 = check_val(col_values[323], False)
                    college.average_net_price_pub_110_plus = check_val(col_values[324], False)
                    college.average_net_price_priv_30 = check_val(col_values[325], False)
                    college.average_net_price_priv_48 = check_val(col_values[326], False)
                    college.average_net_price_priv_75 = check_val(col_values[327], False)
                    college.average_net_price_priv_110 = check_val(col_values[328], False)
                    college.average_net_price_priv_110_plus = check_val(col_values[329], False)

                    # aid
                    college.pell_grand = check_val(col_values[385], False)
                    college.federal_loan = check_val(col_values[437], False)
                    college.debt_completed = check_val(col_values[1503], False)
                    college.debt_completed_median = check_val(col_values[1504], False)
                    college.debt_not_completed = check_val(col_values[1505], False)
                    college.monthly_payments = check_val(col_values[1531], False)

                    # completion
                    college.completion_rate_four_year = check_val(col_values[386], False)
                    college.completion_rate_less_four_year = check_val(col_values[387], False)
                    college.completion_rate_four_year_pooled = check_val(col_values[388], False)
                    college.completion_rate_less_four_year_pooled = check_val(col_values[389], False)
                    college.retention_rate_four_year_pooled = check_val(col_values[1815], False)
                    college.retention_rate_less_four_year_pooled = check_val(col_values[1816], False)

                    # earnings
                    college.mean_earnings = check_val(col_values[1638], False)
                    college.median_earnings = check_val(col_values[1639], False)

                    # student
                    college.undergrad_students = check_val(col_values[290], False)
                    college.students_white = check_val(col_values[292], False)
                    college.students_black = check_val(col_values[293], False)
                    college.students_hispanic = check_val(col_values[294], False)
                    college.students_asian = check_val(col_values[295], False)
                    college.students_native = check_val(col_values[296], False)
                    college.students_pacific = check_val(col_values[297], False)
                    college.students_multiple_races = check_val(col_values[298], False)
                    college.students_non_resident = check_val(col_values[299], False)
                    college.students_unknown_race = check_val(col_values[300], False)
                    college.students_part_time = check_val(col_values[313], False)
                    college.students_female = check_val(col_values[1609], False)
                    college.students_family_income = check_val(col_values[1614], False)

                    # admission
                    college.admission_rate = check_val(col_values[36], False)
                    college.sat_reading = check_val(col_values[44], False)
                    college.sat_math = check_val(col_values[45], False)
                    college.sat_writing = check_val(col_values[46], False)
                    college.sat_average = check_val(col_values[59], False)
                    college.act_cumulative = check_val(col_values[55], False)
                    college.act_english = check_val(col_values[56], False)
                    college.act_math = check_val(col_values[57], False)
                    college.act_writing = check_val(col_values[58], False)

                    colleges.append(college)
                row_num += 1

            cls.objects.bulk_create(colleges)

    @staticmethod
    def get_column_title(index):
        csv.field_size_limit(sys.maxsize)
        with open(os.path.abspath(os.path.join(BASE_DIR, 'open_data_app', DATA_PATH)), 'r', newline='',
                  encoding='utf-8') as file:

            for row in file:
                col_values = row.split(',')
                try:
                    return col_values[index]
                except IndexError:
                    return 'List index out of range'

    @staticmethod
    def get_column_index(title):
        csv.field_size_limit(sys.maxsize)
        with open(os.path.abspath(os.path.join(BASE_DIR, 'open_data_app', DATA_PATH)), 'r', newline='',
                  encoding='utf-8') as file:

            for row in file:
                col_values = row.split(',')
                for index, value in enumerate(col_values):
                    if value == title:
                        return index
                return 'Not found'

    @staticmethod
    def get_dict():
        """
        Returns dictionary of titles for college properties
        :return dict:
        """
        try:
            content = Dictionary.objects.get(name='property_titles').content
            if content is not None:
                return content
            else:
                return {}
        except ObjectDoesNotExist:
            return {}

    @staticmethod
    def get_disciplines():
        """
        Returns slugs of college disciplines
        :return list:
        """
        try:
            content = Dictionary.objects.get(name='discipline_slugs').content
            if content is not None:
                return content
            else:
                return []
        except ObjectDoesNotExist:
            return []

    @staticmethod
    def get_binary_params():
        """
        Returns list of binary (yes/no) filter parameters
        :return list:
        """
        try:
            content = Dictionary.objects.get(name='binary_params').content
            if content is not None:
                return list(content.keys())
            else:
                return []
        except ObjectDoesNotExist:
            return []

    @classmethod
    def create_new_params_dict(cls, params_dict):
        disciplines = cls.get_disciplines()
        new_params_dict = dict()

        for key in params_dict:

            value = params_dict[key]
            try:
                if isinstance(value, list):
                    value_is_int = isinstance(int(value[0]), int)
                else:
                    value_is_int = isinstance(int(value), int)

            except Exception as e:
                print(e)
                value_is_int = False

            if key in disciplines:
                new_key = '{}__gt'.format(key)
                new_params_dict[new_key] = value
            elif key not in ['city', 'city_slug'] and '__slug' not in key and not value_is_int:
                new_key = '{}__slug'.format(key)
                new_params_dict[new_key] = value
            else:
                new_params_dict[key] = value
        return new_params_dict

    @classmethod
    def get_filters(cls, colleges, excluded_filters=[], get_filter=''):
        """
        :param colleges: colleges query set
        :param excluded_filters: filters that should not be returned
        :param get_filter: specific filter's name to return
        :return:
        """

        states, cities, ownership, locales, degrees, carnegie, religions, levels, hist_black, predom_black, hispanic, \
        men_only, women_only, online_only, cur_operating = College.get_values(colleges)

        bin_params = Dictionary.objects.get(name='binary_params').content

        try:
            filters = {
                'multi_val_filters': {
                    'state': [states, 'State'],
                    'city': [cities, 'City/town'],
                    'locale': [locales, 'Locale'],
                    'ownership': [ownership, 'Ownership'],
                    'level': [levels, 'Level'],
                    'degree': [degrees, 'Highest Degree'],
                    'carnegie': [carnegie, 'Carnegie Basic'],
                    'religion': [religions, 'Religious affiliation'],
                },
                'binary_filters': {
                    'hist_black': [hist_black, bin_params['hist_black']],
                    'predom_black': [predom_black, bin_params['predom_black']],
                    'hispanic': [hispanic, bin_params['hispanic']],
                    'men_only': [men_only, bin_params['men_only']],
                    'women_only': [women_only, bin_params['women_only']],
                    'online_only': [online_only, bin_params['online_only']],
                    'cur_operating': [cur_operating, bin_params['cur_operating']], },
            }
        except KeyError:
            filters = {}

        dict = cls.get_dict()
        disciplines = cls.get_disciplines()
        # adding academics filters
        for discipline in disciplines:
            filter = '{}__gt'.format(discipline)
            if colleges.filter(**{filter: 0}).count() > 0:
                try:
                    filters['academics'].append([discipline, dict[discipline]])
                except:
                    filters['academics'] = []
                    filters['academics'].append([discipline, dict[discipline]])

        if len(excluded_filters) > 0:
            for i in excluded_filters:
                try:
                    if filters[i]:
                        filters[i] = []
                except:
                    for a in filters['academics']:
                        if i in a:
                            filters['academics'].remove(a)
                            break

        if len(get_filter) > 0:
            for i in filters:
                if i == get_filter:
                    return filters[i]

        return filters

    @classmethod
    def get_param_text_val(cls, entity, entity_id, param_name, param_value):
        """
        Searches the field by parameter's name and returns a text representation of parameter's value

        :param entity: a state or region
        :param entity_id:
        :param param_name: name of a filter parameter
        :param param_value: value of a filter parameter
        :return str:
        """
        college_fields = cls._meta.get_fields()

        for field in college_fields:
            if param_name == field.name:

                # for relational fields get related object
                if field.related_model is not None:
                    rel_obj_exists = field.related_model.objects.filter(slug=param_value).exists()

                    if rel_obj_exists:
                        rel_obj = field.related_model.objects.get(slug=param_value)

                        # get relational field text value
                        try:
                            param_text_value = rel_obj.description
                        except AttributeError:
                            param_text_value = rel_obj.name

                        # get link for parameter's filter page
                        if param_name == 'state':
                            param_page_link = reverse('college_app:state', kwargs={'state_slug': rel_obj.slug, })
                        elif param_name == 'region':
                            param_page_link = reverse('college_app:region', kwargs={'region_slug': rel_obj.slug, })
                        else:
                            param_page_link = reverse('college_app:filter_values',
                                                      kwargs={'param_name': param_name, 'param_value': param_value})

                # for non-relational fields (city) get query value
                elif param_name in ['city', 'city_slug']:

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

                    param_page_link = reverse('college_app:filter_values',
                                              kwargs={'param_name': param_name, 'param_value': param_value})

                    if len(query_field) > 0:
                        param_text_value = query_field[0]['city']
                        return param_text_value, param_page_link
                    else:
                        return '', ''

                # params without value (academics)
                elif param_name in cls.get_disciplines():
                    dictionary = cls.get_dict()
                    param_text_value = dictionary[param_name]
                    param_page_link = reverse('college_app:filter_no_values', kwargs={'param_name': param_name,})

                # yes/no queries
                else:
                    dictionary = cls.get_dict()
                    param_text_value = dictionary[param_name][int(param_value)]
                    param_page_link = reverse('college_app:filter_values',
                                   kwargs={'param_name': param_name, 'param_value': param_value})

                try:
                    return param_text_value, param_page_link
                except UnboundLocalError:
                    pass
        else:
            return '', ''

    @classmethod
    def get_param_slug_val(cls, param_name, param_id_value):
        """
        The methods retrieves object's slug by it's id
        :param param_name:
        :param param_id_value:
        :return str:
        """
        college_fields = cls._meta.get_fields()

        for field in college_fields:
            if param_name == field.name:

                if field.related_model is not None:
                    rel_obj_exists = field.related_model.objects.filter(pk=param_id_value).exists()

                    if rel_obj_exists:
                        rel_obj = field.related_model.objects.get(pk=param_id_value)

                        try:
                            param_slug_value = rel_obj.slug
                        except AttributeError:
                            param_slug_value = ''

                        return param_slug_value
        else:
            return ''

    @staticmethod
    def get_aggregate_data(colleges):
        average_tuition = colleges.aggregate(Avg('in_state_tuition'))

        max_tuition = colleges.aggregate(Max('in_state_tuition'))
        max_tuition_colleges = colleges.filter(in_state_tuition=max_tuition['in_state_tuition__max'])

        min_tuition = colleges.aggregate(Min('in_state_tuition'))
        min_tuition_colleges = colleges.filter(in_state_tuition=min_tuition['in_state_tuition__min'])

        average_payments = colleges.aggregate(Avg('monthly_payments'))

        max_payments = colleges.aggregate(Max('monthly_payments'))
        max_payments_colleges = colleges.filter(monthly_payments=max_payments['monthly_payments__max'])

        min_payments = colleges.aggregate(Min('monthly_payments'))
        min_payments_colleges = colleges.filter(monthly_payments=min_payments['monthly_payments__min'])

        average_earnings = colleges.aggregate(Avg('median_earnings'))

        max_earnings = colleges.aggregate(Max('median_earnings'))
        max_earnings_colleges = colleges.filter(median_earnings=max_earnings['median_earnings__max'])

        min_earnings = colleges.aggregate(Min('median_earnings'))
        min_earnings_colleges = colleges.filter(median_earnings=min_earnings['median_earnings__min'])

        max_undergrad = colleges.aggregate(Max('undergrad_students'))
        max_admission_rate = colleges.aggregate(Max('admission_rate'))

        return {
            'average_tuition': average_tuition['in_state_tuition__avg'],
            'max_tuition': max_tuition['in_state_tuition__max'],
            'max_tuition_colleges': max_tuition_colleges,
            'min_tuition': min_tuition['in_state_tuition__min'],
            'min_tuition_colleges': min_tuition_colleges,
            'average_payments': average_payments['monthly_payments__avg'],
            'max_payments': max_payments['monthly_payments__max'],
            'max_payments_colleges': max_payments_colleges,
            'min_payments': min_payments['monthly_payments__min'],
            'min_payments_colleges': min_payments_colleges,
            'average_earnings': average_earnings['median_earnings__avg'],
            'max_earnings': max_earnings['median_earnings__max'],
            'max_earnings_colleges': max_earnings_colleges,
            'min_earnings': min_earnings['median_earnings__min'],
            'min_earnings_colleges': min_earnings_colleges,
            'max_undergrad': max_undergrad['undergrad_students__max'],
            'max_admission_rate': max_admission_rate['admission_rate__max'],
        }

    @staticmethod
    def sort_colleges(request, colleges):
        try:
            sort = request.GET['sort']
            if sort:
                is_desc = sort[0] == '-'
                if is_desc:
                    sort = sort[1:]
                    colleges = colleges.order_by(F(sort).desc(nulls_last=True))
                else:
                    colleges = colleges.order_by(F(sort).asc(nulls_last=True))
            return colleges
        except Exception as e:
            print(e)
            return colleges

    def get_absolute_path(self):
        id = self.id
        slug = self.slug

        url = reverse('college_app:college', kwargs={'college_id': id,
                                                     'college_slug': slug,
                                                     })
        return url

    @staticmethod
    def get_map_labels(colleges):
        map_labels = colleges.values_list('latitude', 'longitude', 'name', 'city', 'state__name').exclude(latitude=None)
        return list(map(list, map_labels))

    @classmethod
    def get_values(cls, filtered_colleges=''):

        if filtered_colleges:
            colleges = filtered_colleges
        else:
            colleges = cls.objects.all()

        cities = colleges.values_list('city',
                                      'city_slug').order_by('city').exclude(city=None).distinct()
        states = colleges.values_list('state__name',
                                      'state__slug').order_by('state__name').exclude(
            state__name=None).distinct()
        ownership = colleges.values_list('ownership__description',
                                         'ownership__slug').order_by('ownership__id').exclude(
            ownership__description=None).exclude(
            ownership__description='Not applicable').distinct()
        locales = colleges.values_list('locale__description',
                                       'locale__slug').order_by('locale__id').exclude(
            locale__description=None).exclude(
            locale__description='Not applicable').distinct()
        degrees = colleges.values_list('degree__description',
                                       'degree__slug').order_by(
            'degree__id').exclude(degree__description=None).exclude(
            degree__description='Not applicable').distinct()
        carnegie = colleges.values_list('carnegie__description',
                                        'carnegie__slug').order_by(
            'carnegie').exclude(carnegie__description=None).exclude(
            carnegie__description='Not applicable').distinct()
        religions = colleges.values_list('religion__name',
                                         'religion__slug').order_by(
            'religion__name').exclude(religion__name=None).distinct()
        levels = colleges.values_list('level__description',
                                      'level__slug').order_by('level__id').distinct()
        hist_black = colleges.values('hist_black').order_by('hist_black').exclude(hist_black=None).distinct()
        predom_black = colleges.values('predom_black').order_by('predom_black').exclude(predom_black=None).distinct()
        hispanic = colleges.values('hispanic').order_by('hispanic').exclude(hispanic=None).distinct()
        men_only = colleges.values('men_only').order_by('men_only').exclude(men_only=None).distinct()
        women_only = colleges.values('women_only').order_by('women_only').exclude(women_only=None).distinct()
        online_only = colleges.values('online_only').order_by('online_only').exclude(online_only=None).distinct()
        cur_operating = colleges.values('cur_operating').order_by('cur_operating').exclude(cur_operating=None).distinct()

        return states, cities, ownership, locales, degrees, carnegie, religions, levels, hist_black, predom_black, hispanic, men_only, women_only, online_only, cur_operating

    @staticmethod
    def check_result_is_multiple(colleges):
        if colleges.count() > 1:
            return True

        return False
