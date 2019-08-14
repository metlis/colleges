from django.db import models
from jsonfield import JSONField


class Dictionary(models.Model):
    name = models.CharField(max_length=255, blank=False)
    content = JSONField(blank=True, null=True)