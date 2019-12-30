from open_data_app.models.page import Page
from django.http import Http404
from django.shortcuts import render
from settings import *


def show_content_page(request, page_url):
    if not Page.objects.filter(url=page_url).exists():
        raise Http404()

    page = Page.objects.get(url=page_url)

    # ids of favourite colleges
    favourite_colleges = []
    if 'favourite_colleges' in request.session:
        favourite_colleges = request.session['favourite_colleges']

    cookie_agreement = ''
    if 'cookie_agreement' in request.session:
        cookie_agreement = True

    return render(request, 'content-page.html', {
        'name': page.name,
        'seo_title': page.title,
        'seo_description': page.description,
        'top': page.top_text,
        'bottom': page.bottom_text,
        'favourite_colleges': favourite_colleges,
        'cookie_agreement': cookie_agreement,
        'version': STATIC_VERSION,
    })
