from django.shortcuts import render
from open_data_app.models import College
from settings import *

def index(request):
    colleges = College.objects.all()[:20]
    return render(request, 'index.html', {'colleges': colleges})