from django.contrib import admin
from open_data_app.models.college import College
from open_data_app.models.region import Region
from open_data_app.models.state import State
from open_data_app.models.dictionary import Dictionary
from open_data_app.models.rating import Rating
from open_data_app.models.filter import Filter
from open_data_app.models.template import Template
from open_data_app.models.page import Page


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'region')
    list_filter = ['state', 'region']
    search_fields = ['name']


class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FilterAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    filter_horizontal = ('filters',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(College, CollegeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Page, PageAdmin)
