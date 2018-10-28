from django.db import models


class Carnegie(models.Model):
    code_num = models.IntegerField(null=True)
    description = models.CharField(max_length=255)