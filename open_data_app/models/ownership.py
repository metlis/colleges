from django.db import models, transaction
from django.utils.text import slugify


class Ownership(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.description

    @classmethod
    def save_ownership_slugs(cls):
        ownerships = cls.objects.all()

        with transaction.atomic():
            for ownership in ownerships:
                ownership.slug = slugify(ownership.description)
                ownership.save()