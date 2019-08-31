from django.db import models, transaction
from django.utils.text import slugify


class Religion(models.Model):
    code_num = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_religion_slugs(cls):
        religions = cls.objects.all()

        with transaction.atomic():
            for religion in religions:
                religion.slug = slugify(religion.name)
                religion.save()