from django.urls import path
from open_data_app.api.request_map_labels import request_map_labels
from open_data_app.api.modify_favourites import modify_favourites
from open_data_app.api.request_user_colleges import request_user_colleges
from open_data_app.api.request_map_api_key import request_map_api_key
from open_data_app.api.agree_on_cookies import agree_on_cookies

urlpatterns = [
    path(r'request_map_labels/', request_map_labels, name='request_map_labels'),
    path(r'modify_favourites/', modify_favourites, name='modify_favourites'),
    path(r'request_user_colleges/', request_user_colleges, name='request_user_colleges'),
    path(r'request_map_api_key/', request_map_api_key, name='request_map_api_key'),
    path(r'agree_on_cookies/', agree_on_cookies, name='agree_on_cookies'),
]