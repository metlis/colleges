from django.db import models
import csv
import os
import sys
import urllib.parse
import re
from settings import *


class College(models.Model):
    # school section
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    state = models.IntegerField(null=True)
    region = models.IntegerField(null=True)
    ownership = models.IntegerField(null=True)
    locale = models.IntegerField(null=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    highest_grad_degree = models.IntegerField(null=True)
    camegie_basic = models.IntegerField(null=True)
    hist_black = models.IntegerField(null=True)
    predom_black = models.IntegerField(null=True)
    hispanic = models.IntegerField(null=True)
    men_only = models.IntegerField(null=True)
    women_only = models.IntegerField(null=True)
    religous = models.IntegerField(null=True)
    online_only = models.IntegerField(null=True)
    inst_level = models.IntegerField(null=True)
    cur_operating = models.IntegerField(null=True)

    full_data = models.TextField()

    @classmethod
    def parse_csv(cls):
        csv.field_size_limit(sys.maxsize)
        with open(os.path.abspath(os.path.join(BASE_DIR, 'open_data_app', 'static/data.csv')), 'r', newline='',
                  encoding='utf-8') as file:
            # reader = csv.reader(file, delimiter=',', quotechar='|')

            colleges = []
            row_num = 1
            for row in file:
                if row_num > 1:
                    col_values = row.split(',')

                    if len(col_values) != 1847:
                        # encoded = re.sub(r'(".*?")', r'\1', row)

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


                    def check_val(val):
                        if val == 'NULL':
                            return None
                        else:
                            return val

                    college = cls()
                    college.id = col_values[0]
                    college.name = col_values[3]
                    college.city = col_values[4]
                    college.zip = col_values[6]
                    college.state = check_val(col_values[17])
                    college.region = check_val(col_values[18])
                    college.ownership = check_val(col_values[16])
                    college.locale = check_val(col_values[19])
                    college.latitude = check_val(col_values[21])
                    college.longitude = check_val(col_values[22])
                    college.highest_grad_degree = check_val(col_values[15])
                    college.camegie_basic = check_val(col_values[23])
                    college.hist_black = check_val(col_values[26])
                    college.predom_black = check_val(col_values[27])
                    college.hispanic = check_val(col_values[31])
                    college.men_only = check_val(col_values[33])
                    college.women_only = check_val(col_values[34])
                    college.religous = check_val(col_values[35])
                    college.online_only = check_val(col_values[289])
                    college.inst_level = check_val(col_values[1738])
                    college.cur_operating = check_val(col_values[315])
                    college.full_data = ','.join(col_values)

                    colleges.append(college)
                row_num += 1
                print(row_num)

            cls.objects.bulk_create(colleges)
