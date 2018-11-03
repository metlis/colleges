from django.urls import path

from open_data_app.views.college import get_college, get_college_slug
from open_data_app.views.region import get_region, get_region_slug
from open_data_app.views.state import get_state, get_state_slug, get_city_slug
from open_data_app.views.index import index

app_name = 'college_app'

urlpatterns = [
    path(r'state/<int:state_id>/', get_state, name='state'),
    path(r'state/<int:state_id>/<slug:state_slug>/', get_state_slug, name='state_slug'),
    path(r'state/<int:state_id>/<slug:state_slug>/<param>/<param_value>/', get_city_slug, name='state_param'),

    path(r'region/<int:region_id>/', get_region, name='region'),
    path(r'region/<int:region_id>/<slug:region_slug>/', get_region_slug, name='region_slug'),

    path(r'college/<int:college_id>/', get_college, name='college'),
    path(r'college/<int:college_id>/<slug:college_slug>/', get_college_slug, name='college_slug'),

    path(r'', index, name='index'),
]
