from django.shortcuts import render


def show_favourite(request):
    return render(request, 'favourite.html')