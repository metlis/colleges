from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=255, blank=False)
    url = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    top_text = models.TextField(blank=True)
    bottom_text = models.TextField(blank=True)
