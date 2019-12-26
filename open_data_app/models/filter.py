from django.db import models
from open_data_app.models.state import State
from open_data_app.models.region import Region
from open_data_app.models.ownership import Ownership
from open_data_app.models.locale import Locale
from open_data_app.models.degree import Degree
from open_data_app.models.carnegie import Carnegie
from open_data_app.models.religion import Religion
from open_data_app.models.level import Level


class Filter(models.Model):
    name = models.CharField(max_length=255, blank=False)
    items_quantity = models.IntegerField(blank=True)
    order = models.CharField(max_length=255, null=True)
    parameter_name = models.CharField(max_length=255, null=True, blank=True)
    parameter_value = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    ownership = models.ForeignKey(Ownership, on_delete=models.CASCADE, null=True, blank=True)
    locale = models.ForeignKey(Locale, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    carnegie = models.ForeignKey(Carnegie, on_delete=models.CASCADE, null=True, blank=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name