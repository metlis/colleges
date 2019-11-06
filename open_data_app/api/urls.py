from django.urls import path
from open_data_app.api.get_labels import get_labels
from open_data_app.api.modify_favourites import modify_favourites
from open_data_app.api.get_favourites import get_favourites
from open_data_app.api.get_map_api_key import get_map_api_key
from open_data_app.api.agree_on_cookies import agree_on_cookies

urlpatterns = [
    path(r'get_labels/', get_labels, name='get_labels'),
    path(r'modify_favourites/', modify_favourites, name='modify_favourites'),
    path(r'get_favourites/', get_favourites, name='get_favourites'),
    path(r'get_map_api_key/', get_map_api_key, name='get_map_api_key'),
    path(r'agree_on_cookies/', agree_on_cookies, name='agree_on_cookies'),
]