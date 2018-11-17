from django.db import models


class Religion(models.Model):
    code_num = models.IntegerField(null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name