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
from django.db.models import Avg, Max, Min, F
from django.urls import reverse


class College(models.Model):
    # school section
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    city_slug = models.SlugField(max_length=255, blank=True, verbose_name='city')
    zip = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    calc_url = models.CharField(max_length=255, blank=True)
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
    public_administration_social_service = models.FloatField(null=True,
                                                             verbose_name='public_administration_social_service')
    science_technology = models.FloatField(null=True, verbose_name='science_technology')
    social_science = models.FloatField(null=True, verbose_name='social_science')
    theology_religious_vocation = models.FloatField(null=True, verbose_name='theology_religious_vocation')
    transportation = models.FloatField(null=True, verbose_name='transportation')
    visual_performing = models.FloatField(null=True, verbose_name='visual_performing')

    # cost
    average_net_price_public = models.FloatField(null=True, verbose_name='average_net_price_public')
    average_net_price_private = models.FloatField(null=True, verbose_name='average_net_price_private')
    average_cost_of_attendance_academic = models.FloatField(null=True,
                                                            verbose_name='average_cost_of_attendance_academic')
    average_cost_of_attendance_program = models.FloatField(null=True, verbose_name='average_cost_of_attendance_program')
    in_state_tuition = models.FloatField(null=True, verbose_name='in_state_tuition')
    out_state_tuition = models.FloatField(null=True, verbose_name='out_state_tuition')
    average_net_price_pub_30 = models.FloatField(null=True, verbose_name='average_net_price_pub_30')
    average_net_price_pub_48 = models.FloatField(null=True, verbose_name='average_net_price_pub_48')
    average_net_price_pub_75 = models.FloatField(null=True, verbose_name='average_net_price_pub_75')
    average_net_price_pub_110 = models.FloatField(null=True, verbose_name='average_net_price_pub_110')
    average_net_price_pub_110_plus = models.FloatField(null=True, verbose_name='average_net_price_pub_110_plus')
    average_net_price_priv_30 = models.FloatField(null=True, verbose_name='average_net_price_priv_30')
    average_net_price_priv_48 = models.FloatField(null=True, verbose_name='average_net_price_priv_48')
    average_net_price_priv_75 = models.FloatField(null=True, verbose_name='average_net_price_priv_75')
    average_net_price_priv_110 = models.FloatField(null=True, verbose_name='average_net_price_priv_110')
    average_net_price_priv_110_plus = models.FloatField(null=True, verbose_name='average_net_price_priv_110_plus')

    # aid
    pell_grand = models.FloatField(null=True, verbose_name='pell_grand')
    federal_loan = models.FloatField(null=True, verbose_name='federal_loan')
    debt_completed = models.FloatField(null=True, verbose_name='debt_completed')
    debt_not_completed = models.FloatField(null=True, verbose_name='debt_not_completed')
    debt_completed_median = models.FloatField(null=True, verbose_name='debt_completed_median')
    monthly_payments = models.FloatField(null=True, verbose_name='monthly_payments')

    # completion
    completion_rate_four_year = models.FloatField(null=True, verbose_name='completion_rate_four_year')
    completion_rate_less_four_year = models.FloatField(null=True, verbose_name='completion_rate_less_four_year')
    completion_rate_four_year_pooled = models.FloatField(null=True, verbose_name='completion_rate_four_year_pooled')
    completion_rate_less_four_year_pooled = models.FloatField(null=True, verbose_name='completion_rate_less_four_year_pooled')
    retention_rate_four_year_pooled = models.FloatField(null=True, verbose_name='retention_rate_four_year_pooled')
    retention_rate_less_four_year_pooled = models.FloatField(null=True,
                                                              verbose_name='retention_rate_less_four_year_pooled')

    # earnings
    mean_earnings = models.FloatField(null=True, verbose_name='mean_earnings')
    median_earnings = models.FloatField(null=True, verbose_name='median_earnings')

    # student
    undergrad_students = models.FloatField(null=True, verbose_name='undergrad_students')
    students_white = models.FloatField(null=True, verbose_name='students_white')
    students_black = models.FloatField(null=True, verbose_name='students_black')
    students_hispanic = models.FloatField(null=True, verbose_name='students_hispanic')
    students_asian = models.FloatField(null=True, verbose_name='students_asian')
    students_native = models.FloatField(null=True, verbose_name='students_native')
    students_pacific = models.FloatField(null=True, verbose_name='students_pacific')
    students_multiple_races = models.FloatField(null=True, verbose_name='students_multiple_races')
    students_non_resident = models.FloatField(null=True, verbose_name='students_non_resident')
    students_unknown_race = models.FloatField(null=True, verbose_name='students_unknown_race')
    students_part_time = models.FloatField(null=True, verbose_name='students_part_time')
    students_female = models.FloatField(null=True, verbose_name='students_female')
    students_family_income = models.FloatField(null=True, verbose_name='students_family_income')

    # admission
    admission_rate = models.FloatField(null=True, verbose_name='admission_rate')
    sat_reading = models.FloatField(null=True, verbose_name='sat_reading')
    sat_math = models.FloatField(null=True, verbose_name='sat_math')
    sat_writing = models.FloatField(null=True, verbose_name='sat_writing')
    sat_average = models.FloatField(null=True, verbose_name='sat_average')
    act_cumulative = models.FloatField(null=True, verbose_name='act_cumulative')
    act_english = models.FloatField(null=True, verbose_name='act_english')
    act_math = models.FloatField(null=True, verbose_name='act_math')
    act_writing = models.FloatField(null=True, verbose_name='act_writing')

    class Meta:
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['region']),
            models.Index(fields=['ownership']),
            models.Index(fields=['locale']),
            models.Index(fields=['highest_grad_degree']),
            models.Index(fields=['carnegie_basic']),
            models.Index(fields=['inst_level']),
            models.Index(fields=['agriculture']),
            models.Index(fields=['architecture']),
            models.Index(fields=['ethnic_cultural_gender']),
            models.Index(fields=['business_marketing']),
            models.Index(fields=['communication']),
            models.Index(fields=['communications_technology']),
            models.Index(fields=['computer']),
            models.Index(fields=['construction']),
            models.Index(fields=['education']),
            models.Index(fields=['engineering']),
            models.Index(fields=['engineering_technology']),
            models.Index(fields=['english']),
            models.Index(fields=['family_consumer_science']),
            models.Index(fields=['language']),
            models.Index(fields=['health']),
            models.Index(fields=['history']),
            models.Index(fields=['security_law_enforcement']),
            models.Index(fields=['legal']),
            models.Index(fields=['humanities']),
            models.Index(fields=['library']),
            models.Index(fields=['mathematics']),
            models.Index(fields=['mechanic_repair_technology']),
            models.Index(fields=['military']),
            models.Index(fields=['multidiscipline']),
            models.Index(fields=['resources']),
            models.Index(fields=['parks_recreation_fitness']),
            models.Index(fields=['personal_culinary']),
            models.Index(fields=['philosophy_religious']),
            models.Index(fields=['physical_science']),
            models.Index(fields=['precision_production']),
            models.Index(fields=['psychology']),
            models.Index(fields=['public_administration_social_service']),
        ]

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

                # for checking column name:
                # col_values = row.split(',')
                # print(col_values[314])
                # return

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
                        if (val == 'NULL' or val == 'PrivacySuppressed') and not str:
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
                    college.calc_url = check_val(col_values[9], True)
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

    @classmethod
    def get_dict(cls):
        dict = {'hist_black': ['Historically not black', 'Historically black'],
                'predom_black': ['Predominantely not black', 'Predominantely black'],
                'hispanic': ['Predominantely not hispanic', 'Predominantely hispanic'],
                'men_only': ['Not men-only', 'Men-only'],
                'women_only': ['Not women-only', 'Women-only'],
                'online_only': ['Not online-only', 'Online-only'],
                'cur_operating': ['Currently closed', 'Currently operating'],
                'agriculture': 'Agriculture, Agriculture Operations, and Related Sciences',
                'architecture': 'Architecture and Related Services',
                'ethnic_cultural_gender': 'Area, Ethnic, Cultural, Gender, and Group Studies',
                'biological': 'Biological and Biomedical Sciences',
                'business_marketing': 'Business, Management, Marketing, and Related Support Services',
                'communication': 'Communication, Journalism, and Related Programs',
                'communications_technology': 'Communications Technologies/Technicians and Support Services',
                'computer': 'Computer and Information Sciences and Support Services',
                'construction': 'Construction Trades',
                'education': 'Education',
                'engineering': 'Engineering',
                'engineering_technology': 'Engineering Technologies and Engineering-Related Fields',
                'english': 'English Language and Literature/Letters',
                'family_consumer_science': 'Family and Consumer Sciences/Human Sciences',
                'language': 'Foreign Languages, Literatures, and Linguistics',
                'health': 'Health Professions and Related Programs',
                'history': 'History',
                'security_law_enforcement': 'Homeland Security, Law Enforcement, Firefighting and Related Protective Services',
                'legal': 'Legal Professions and Studies',
                'humanities': 'Liberal Arts and Sciences, General Studies and Humanities',
                'library': 'Library Science',
                'mathematics': 'Mathematics and Statistics',
                'mechanic_repair_technology': 'Mechanic and Repair Technologies/Technicians',
                'military': 'Military Technologies and Applied Sciences',
                'multidiscipline': 'Multi/Interdisciplinary Studies',
                'resources': 'Natural Resources and Conservation',
                'parks_recreation_fitness': 'Parks, Recreation, Leisure, and Fitness Studies',
                'personal_culinary': 'Personal and Culinary Services',
                'philosophy_religious': 'Philosophy and Religious Studies',
                'physical_science': 'Physical Sciences',
                'precision_production': 'Precision Production',
                'psychology': 'Psychology',
                'public_administration_social_service': 'Public Administration and Social Service Professions',
                'science_technology': 'Science Technologies/Technicians',
                'social_science': 'Social Sciences',
                'theology_religious_vocation': 'Theology and Religious Vocations',
                'transportation': 'Transportation and Materials Moving',
                'visual_performing': 'Visual and Performing Arts',
                }
        return dict

    @classmethod
    def get_disciplines(cls):
        disciplines = ['agriculture', 'architecture', 'ethnic_cultural_gender', 'biological', 'business_marketing',
                       'communication', 'communications_technology', 'computer', 'construction', 'education',
                       'engineering', 'engineering_technology', 'english', 'family_consumer_science', 'language',
                       'health', 'history', 'security_law_enforcement', 'legal', 'humanities', 'library', 'mathematics',
                       'mechanic_repair_technology', 'military', 'multidiscipline', 'resources',
                       'parks_recreation_fitness', 'personal_culinary', 'philosophy_religious', 'physical_science',
                       'precision_production', 'psychology', 'public_administration_social_service',
                       'science_technology', 'social_science', 'theology_religious_vocation', 'transportation',
                       'visual_performing']
        return disciplines

    @classmethod
    def create_new_params_dict(cls, params_dict):
        disciplines = cls.get_disciplines()
        new_params_dict = params_dict.copy()
        for key in new_params_dict:
            if key in disciplines:
                new_key = '{}__gt'.format(key)
                new_params_dict[new_key] = new_params_dict[key]
                new_params_dict.pop(key)
        return new_params_dict

    @classmethod
    def get_filters(cls, colleges, excluded_filters=[], get_filter=''):
        """

        :param colleges: colleges query set
        :param excluded_filters: filters that should not be returned
        :param get_filter: specific filter's name to return
        :return:
        """

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
                # params without value (academics)
                elif param in cls.get_disciplines():
                    dict = cls.get_dict()
                    query_val = dict[param]
                # yes/no queries
                else:
                    dict = cls.get_dict()
                    query_val = dict[param][int(param_value)]

                try:
                    return param, query_val, field._verbose_name, param_value
                except:
                    pass
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    @classmethod
    def get_aggregate_data(cls, colleges):
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

    @classmethod
    def sort_colleges(cls, request, colleges):
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
        except:
            return colleges

    def get_absolute_path(self):
        id = self.id
        slug = self.slug

        url = reverse('college_app:college_slug', kwargs={'college_id': id,
                                                      'college_slug': slug,
                                                      })
        return url

    @classmethod
    def get_map_labels(cls, colleges):
        map_labels = colleges.values_list('latitude', 'longitude', 'name', 'city', 'state__name').exclude(latitude=None)
        return list(map(list, map_labels))