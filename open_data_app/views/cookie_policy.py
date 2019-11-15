from django.shortcuts import render
from settings import DOMAIN


def cookie_policy(request):
    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    return render(request, 'cookie-policy.html', {
        'domain': DOMAIN,
        'cookie_agreement': cookie_agreement,
    })