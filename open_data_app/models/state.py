from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_state_data(cls, state_id):
        state = cls.objects.get(id=state_id)
        state_slug = slugify(state.name)

        return state, state_slug

    def get_absolute_path(self):
        id = self.id
        slug = slugify(self.name)
        url = reverse('college_app:state_slug', kwargs={'state_id': id,
                                                      'state_slug': slug,
                                                      })
        return url