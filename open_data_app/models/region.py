from django.db import models
import re
from django.utils.text import slugify


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_region_data(cls, region_id):
        region = cls.objects.get(id=region_id)
        region_re = re.search('(.*?)\s\((.*?)\)', region.name)
        try:
            region_name = region_re.group(1)
            region_slug = slugify(region_name)
            region_states = region_re.group(2)
        except:
            region_name = ''
            region_slug = ''
            region_states = ''

        return region_name, region_slug, region_states