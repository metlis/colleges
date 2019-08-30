from django.db import models, transaction
from django.utils.text import slugify
from django.urls import reverse


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_path(self):

        try:
            url = reverse('college_app:state', kwargs={'state_id': self.id,
                                                       'state_slug': self.slug,
                                                       })
        except Exception as e:
            print(e)
            url = ''

        return url

    @classmethod
    def save_state_slugs(cls):
        states = cls.objects.all()

        with transaction.atomic():
            for state in states:
                state.slug = slugify(state.name)
                state.save()
