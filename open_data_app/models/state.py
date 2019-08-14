from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_state_slug(self):
        state_slug = slugify(self.name)

        return state_slug

    def get_absolute_path(self):
        id = self.id
        slug = slugify(self.name)
        url = reverse('college_app:state', kwargs={'state_id': id,
                                                       'state_slug': slug,
                                                       })
        return url
