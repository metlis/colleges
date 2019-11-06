from django.shortcuts import render


def page_not_found(request):
    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    return render(request, '404.html', {
        'favourite_colleges': favourite_colleges,
        'cookie_agreement': cookie_agreement,
    })
