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
    degrees = College.objects.values_list('highest_grad_degree__id',
                                            'highest_grad_degree__description').order_by(
        'highest_grad_degree__id').exclude(highest_grad_degree__description=None).exclude(
        highest_grad_degree__description='Not applicable').distinct()
    carnegie_basic = College.objects.values_list('carnegie_basic__id',
                                                   'carnegie_basic__description').order_by(
        'carnegie_basic__description').exclude(carnegie_basic__description=None).exclude(
        carnegie_basic__description='Not applicable').distinct()
    religions = College.objects.values_list('religous__id',
                                              'religous__name').order_by(
        'religous__name').exclude(religous__name=None).distinct()
    levels = College.objects.values_list('inst_level__id',
                                           'inst_level__description').order_by('inst_level__id').distinct()
    return render(request, 'index.html', {'states': states,
                                          'regions': regions,
                                          'ownership': ownership,
                                          'locales': locales,
                                          'degrees': degrees,
                                          'carnegie_basic': carnegie_basic,
                                          'religions': religions,
                                          'levels': levels,
                                          })