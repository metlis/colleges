from django.db import models


class Locale(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)