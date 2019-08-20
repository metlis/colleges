from django.shortcuts import render
from open_data_app.models import College
from open_data_app.models import State
from open_data_app.models import Region
from settings import *


def index(request):
    states = State.objects.all()
    regions = Region.objects.all()
    ownership = College.objects.values_list('ownership__id',
                                            'ownership__description').order_by('ownership__id').exclude(
        ownership__description=None).exclude(
        ownership__description='Not applicable').distinct()
    locales = College.objects.values_list('locale__id',
                                          'locale__description').order_by('locale__id').exclude(
        locale__description=None).exclude(
        locale__description='Not applicable').distinct()
    degrees = College.objects.values_list('degree__id',
                                          'degree__description').order_by(
        'degree__id').exclude(degree__description=None).exclude(
        degree__description='Not applicable').distinct()
    carnegie = College.objects.values_list('carnegie__id',
                                           'carnegie__description').order_by(
        'carnegie__description').exclude(carnegie__description=None).exclude(
        carnegie__description='Not applicable').distinct()
    religions = College.objects.values_list('religion__id',
                                            'religion__name').order_by(
        'religion__name').exclude(religion__name=None).distinct()
    levels = College.objects.values_list('level__id',
                                         'level__description').order_by('level__id').distinct()

    dictionary = College.get_dict()
    disciplines = College.get_disciplines()
    academics = []

    for discipline in disciplines:
        academics.append([discipline, dictionary[discipline]])

    return render(request, 'index.html', {'states': states,
                                          'regions': regions,
                                          'ownership': ownership,
                                          'locales': locales,
                                          'degrees': degrees,
                                          'carnegie': carnegie,
                                          'religions': religions,
                                          'levels': levels,
                                          'disciplines': academics,
                                          })
