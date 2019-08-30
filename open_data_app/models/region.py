from django.db import models, transaction
from django.utils.text import slugify
from django.urls import reverse
import re


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def get_region_data(self):
        region_re = re.search('(.*?)\s\((.*?)\)', self.name)

        try:
            region_name = region_re.group(1)
            region_states = region_re.group(2)
            region_slug = self.slug
        except AttributeError:
            region_name = self.name
            region_states = ''
            region_slug = self.slug

        return region_name, region_slug, region_states

    def get_absolute_path(self):

        try:
            url = reverse('college_app:region', kwargs={'region_id': self.id,
                                                        'region_slug': self.slug,
                                                        })
        except Exception as e:
            print(e)
            url = ''

        return url

    @classmethod
    def save_region_slugs(cls):
        regions = cls.objects.all()

        with transaction.atomic():
            for region in regions:
                region_re = re.search('(.*?)\s\((.*?)\)', region.name)

                try:
                    region_name = region_re.group(1)
                except AttributeError:
                    region_name = ''

                region.slug = slugify(region_name)
                region.save()