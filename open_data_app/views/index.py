from django.shortcuts import render
from open_data_app.models import College
from open_data_app.models import State
from open_data_app.models import Region
from settings import *

def index(request):
    states = State.objects.all()
    regions = Region.objects.all()
    return render(request, 'index.html', {'states': states, 'regions': regions})