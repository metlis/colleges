from django.shortcuts import render
from settings import *


def disclaimer(request):
    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    return render(request, 'disclaimer.html', {
        'domain': DOMAIN,
        'cookie_agreement': cookie_agreement,
        'version': STATIC_VERSION,
        'favourite_colleges': favourite_colleges,
    })