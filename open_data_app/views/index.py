from django.shortcuts import render
from open_data_app.models import College
from open_data_app.utils.seo import Seo
from open_data_app.models import State
from open_data_app.models import Region
from settings import *


def index(request):
    regions, states, cities, ownership, locales, degrees, carnegie, religions, levels, hist_black, predom_black, hispanic, \
    men_only, women_only, online_only, cur_operating = College.get_values()

    states = State.objects.all()
    regions = Region.objects.all()
    dictionary = College.get_dict()
    disciplines = College.get_disciplines()
    academics = []

    for discipline in disciplines:
        academics.append([discipline, dictionary[discipline]])

    filters = College.get_filters()

    seo_title = Seo.generate_title('index', '', '')
    seo_description = Seo.generate_description('index', '', '')

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    context = {'states': states,
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
               'favourite_colleges': favourite_colleges,
               'cookie_agreement': cookie_agreement,
               'version': STATIC_VERSION,
               }

    context.update(filters)

    return render(request, 'index.html', context)
