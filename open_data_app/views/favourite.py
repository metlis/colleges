from django.shortcuts import render


def show_favourite(request):
    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    return render(request, 'favourite.html', {'favourite_colleges': favourite_colleges,})