from django.urls import path

from open_data_app.views.college import get_college, get_college_slug
from open_data_app.views.parameter import filter_values
from open_data_app.views.region import get_region, get_region_slug, get_region_param
from open_data_app.views.state import get_state, get_state_slug, get_state_param
from open_data_app.views.index import index
from open_data_app.views.main_filter import main_filter
from open_data_app.views.search import search
from open_data_app.views.no_val_parameter import filter_no_values
from open_data_app.api.get_labels import get_labels
from open_data_app.api.modify_favourites import modify_favourites
from open_data_app.modules.sitemap import CollegesSitemap, StatesSitemap, RegionsSitemap, DisciplinesSitemap, \
    FilterParamsSitemap, StateFilterParamsSitemap, RegionFilterParamsSitemap
from django.contrib.sitemaps.views import sitemap

app_name = 'college_app'

# sitemaps = {
#     'regions': RegionsSitemap,
#     'regions_params': RegionFilterParamsSitemap,
#     'states': StatesSitemap,
#     'states_params': StateFilterParamsSitemap,
#     'disciplines': DisciplinesSitemap,
#     'filters': FilterParamsSitemap,
#     'colleges': CollegesSitemap,
# }

handler404 = 'open_data_app.views.page_not_found'
urlpatterns = [
    path(r'state/<int:state_id>/', get_state, name='state'),
    path(r'state/<int:state_id>/<slug:state_slug>/', get_state_slug, name='state_slug'),
    path(r'state/<int:state_id>/<slug:state_slug>/<param>/<param_value>/', get_state_param, name='state_param'),

    path(r'region/<int:region_id>/', get_region, name='region'),
    path(r'region/<int:region_id>/<slug:region_slug>/', get_region_slug, name='region_slug'),
    path(r'region/<int:region_id>/<slug:region_slug>/<param>/<param_value>/', get_region_param, name='region_param'),

    path(r'college/<int:college_id>/', get_college, name='college'),
    path(r'college/<int:college_id>/<slug:college_slug>/', get_college_slug, name='college_slug'),

    path(r'param/<param>/', filter_no_values, name='filter_no_values'),
    path(r'param/<param>/<param_value>/', filter_values, name='filter_values'),

    path(r'main/', main_filter, name='main_filter'),

    path(r'search/', search, name='search'),

    path(r'api/get_labels/', get_labels, name='get_labels'),
    path(r'api/modify_favourites/', modify_favourites, name='modify_favourites'),

    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path(r'', index, name='index'),
]
