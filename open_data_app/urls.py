from django.urls import path

from open_data_app.views.index import index

app_name = 'college_app'

urlpatterns = [
    path('', index, name='index'),
]