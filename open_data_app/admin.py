from django.contrib import admin
from open_data_app.models.college import College
from open_data_app.models.region import Region
from open_data_app.models.state import State

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'region')
    list_filter = ['state', 'region']
    search_fields = ['name']

class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(College, CollegeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(State, StateAdmin)

