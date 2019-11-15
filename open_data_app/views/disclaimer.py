from django.shortcuts import render
from settings import DOMAIN


def disclaimer(request):
    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    return render(request, 'disclaimer.html', {
        'domain': DOMAIN,
        'cookie_agreement': cookie_agreement,
    })