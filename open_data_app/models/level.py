from django.db import models, transaction
from django.utils.text import slugify


class Level(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.description

    @classmethod
    def save_as_slug(cls):
        levels = cls.objects.all()

        with transaction.atomic():
            for level in levels:
                level.slug = slugify(level.description)
                level.save()