from django.db import models
import csv
import os
import sys
import urllib.parse
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
    hist_black = models.IntegerField(null=True)
    predom_black = models.IntegerField(null=True)
    hispanic = models.IntegerField(null=True)
    men_only = models.IntegerField(null=True)
    women_only = models.IntegerField(null=True)
    religous = models.ForeignKey(Religion, on_delete=models.PROTECT, null=True, verbose_name='religion')
    online_only = models.IntegerField(null=True)
    inst_level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, verbose_name='level')
    cur_operating = models.IntegerField(null=True)


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

