from django.db import models
from django.utils.text import slugify


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