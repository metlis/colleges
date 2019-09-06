from django.shortcuts import render
from open_data_app.models import College
from open_data_app.modules.seo import Seo
from settings import *


def index(request):

    dictionary = College.get_dict()
    disciplines = College.get_disciplines()
    academics = []

    for discipline in disciplines:
        academics.append([discipline, dictionary[discipline]])

    filters = College.get_filters()

    seo_title = Seo.generate_title('index', '', '')
    seo_description = Seo.generate_description('index', '', '')

    context = {
               'disciplines': academics,
               'seo_title': seo_title,
               'seo_description': seo_description,
               }

    context.update(filters)

    return render(request, 'index.html', context)
