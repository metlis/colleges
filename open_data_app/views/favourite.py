from django.shortcuts import render
from settings import *


def show_favourite(request):
    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    return render(request, 'favourite.html', {
        'favourite_colleges': favourite_colleges,
        'cookie_agreement': cookie_agreement,
        'version': STATIC_VERSION,
    })