from django.shortcuts import render


def page_not_found(request):
    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    return render(request, '404.html', {'favourite_colleges': favourite_colleges,})