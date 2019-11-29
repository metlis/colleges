from django.db import models, transaction
from django.utils.text import slugify


class Carnegie(models.Model):
    code_num = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.description

    @classmethod
    def save_as_slug(cls):
        carnegie_options = cls.objects.all()

        with transaction.atomic():
            for carnegie in carnegie_options:
                carnegie.slug = slugify(carnegie.description)
                carnegie.save()
