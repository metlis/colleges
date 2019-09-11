from django.urls import path, re_path

from open_data_app.views.college import get_college

from open_data_app.views.parameter import filter_values
from open_data_app.views.geo import get_geo, get_geo_param, get_geo_redirect
from open_data_app.views.index import index
from open_data_app.views.main_filter import main_filter
from open_data_app.views.search import search
from open_data_app.views.no_val_parameter import filter_no_values
from open_data_app.api.get_labels import get_labels
from open_data_app.api.modify_favourites import modify_favourites
from open_data_app.views.favourite import show_favourite
from open_data_app.utils.sitemap import CollegesSitemap, StatesSitemap, RegionsSitemap, DisciplinesSitemap, \
    FilterParamsSitemap, StateFilterParamsSitemap, RegionFilterParamsSitemap, CitiesSitemap
from django.contrib.sitemaps.views import sitemap

app_name = 'college_app'

# sitemaps = {
#     'regions': RegionsSitemap,
#     'regions_params': RegionFilterParamsSitemap,
#     'states': StatesSitemap,
#     'states_params': StateFilterParamsSitemap,
#     'disciplines': DisciplinesSitemap,
#     'filters': FilterParamsSitemap,
#     'cities': CitiesSitemap,
#     'colleges': CollegesSitemap,
# }

handler404 = 'open_data_app.views.page_not_found'
urlpatterns = [
    # old geo urls with id
    re_path(r'^(?P<geo_name>state|region)/(?P<geo_id>[0-9]+)/(?P<geo_slug>.*)/(?P<param_name>.*)/(?P<param_value>.*)/$',
            get_geo_redirect, name='geo_param_redirect'),
    re_path(r'^(?P<geo_name>state|region)/(?P<geo_id>[0-9]+)/(?P<geo_slug>.*)/$', get_geo_redirect, name='geo_redirect'),
    # new geo urls
    re_path(r'^(?P<geo_name>state|region)/(?P<geo_slug>.*)/(?P<param_name>.*)/(?P<param_value>.*)/$', get_geo_param,
            name='geo_param'),
    re_path(r'^(?P<geo_name>state|region)/(?P<geo_slug>.*)/$', get_geo, name='geo'),

    path(r'institution/<int:college_id>/<slug:college_slug>/', get_college, name='college'),

    path(r'param/<param_name>/', filter_no_values, name='filter_no_values'),
    path(r'param/<param_name>/<param_value>/', filter_values, name='filter_values'),

    path(r'main/', main_filter, name='main_filter'),

    path(r'search/', search, name='search'),

    path(r'favourite/', show_favourite, name='show_favourite'),

    path(r'api/get_labels/', get_labels, name='get_labels'),
    path(r'api/modify_favourites/', modify_favourites, name='modify_favourites'),

    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path(r'', index, name='index'),
]
