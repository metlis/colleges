from django.urls import path
from open_data_app.api.request_map_labels import request_map_labels
from open_data_app.api.toggle_favourite import toggle_favourite
from open_data_app.api.request_user_colleges import request_user_colleges
from open_data_app.api.request_similar_colleges import request_similar_colleges
from open_data_app.api.request_map_api_key import request_map_api_key
from open_data_app.api.agree_on_cookies import agree_on_cookies

urlpatterns = [
    path(r'request_map_labels/', request_map_labels, name='request_map_labels'),
    path(r'toggle_favourite/', toggle_favourite, name='toggle_favourite'),
    path(r'request_user_colleges/', request_user_colleges, name='request_user_colleges'),
    path(r'request_similar_colleges/', request_similar_colleges, name='request_similar_colleges'),
    path(r'request_map_api_key/', request_map_api_key, name='request_map_api_key'),
    path(r'agree_on_cookies/', agree_on_cookies, name='agree_on_cookies'),
]