from django.db import models
from open_data_app.models.filter import Filter
from open_data_app.models.page import Page


class Rating(Page):
    filters = models.ManyToManyField(Filter)