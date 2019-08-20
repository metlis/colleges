from django.db import models
import re
from django.utils.text import slugify
from django.urls import reverse


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_region_data(self):
        region_re = re.search('(.*?)\s\((.*?)\)', self.name)
        try:
            region_name = region_re.group(1)
            region_slug = slugify(region_name)
            region_states = region_re.group(2)
        except:
            region_name = ''
            region_slug = ''
            region_states = ''

        return region_name, region_slug, region_states

    def get_absolute_path(self):
        id = self.id
        try:
            region_re = re.search('(.*?)\s\((.*?)\)', self.name)
            region_name = region_re.group(1)
            slug = slugify(region_name)
            url = reverse('college_app:region', kwargs={'region_id': id,
                                                        'region_slug': slug,
                                                        })
        except:
            url = ''
        return url