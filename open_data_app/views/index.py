from django.shortcuts import render
from open_data_app.models import College
from open_data_app.models import State
from open_data_app.models import Region
from open_data_app.modules.seo import Seo
from settings import *


def index(request):
    states, cities, ownership, locales, degrees, carnegie, religions, levels, hist_black, predom_black, hispanic, \
    men_only, women_only, online_only, cur_operating = College.get_values()

    states = State.objects.all()
    regions = Region.objects.all()
    dictionary = College.get_dict()
    disciplines = College.get_disciplines()
    academics = []

    for discipline in disciplines:
        academics.append([discipline, dictionary[discipline]])

    seo_title = Seo.generate_title('index', '', '')
    seo_description = Seo.generate_description('index', '', '')

    return render(request, 'index.html', {'states': states,
                                          'regions': regions,
                                          'ownership': ownership,
                                          'locales': locales,
                                          'degrees': degrees,
                                          'carnegie': carnegie,
                                          'religions': religions,
                                          'levels': levels,
                                          'disciplines': academics,
                                          'seo_title': seo_title,
                                          'seo_description': seo_description,
                                          })
