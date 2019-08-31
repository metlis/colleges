from django.db import models, transaction
from django.utils.text import slugify
import re


class Locale(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.description

    @classmethod
    def save_locale_slugs(cls):
        locales = cls.objects.all()

        with transaction.atomic():
            for locale in locales:
                locale_re = re.search('(.+?:\s.+?)\s\(.*?', locale.description)
                locale.slug = slugify(locale_re.group(1))
                locale.save()
