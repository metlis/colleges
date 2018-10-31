from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from open_data_app.models import State
from open_data_app.models import College
from settings import *
from django.utils.text import slugify
import urllib.parse


def get_state(request, state_id):
    state_exist = State.objects.filter(id=state_id).exists()

    if state_exist:
        state = State.objects.get(id=state_id)
        state_slug = slugify(state.name)
        return HttpResponseRedirect(urllib.parse.urljoin(str(state_id), state_slug))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def get_state_slug(request, state_id, state_slug):
    state_exist = State.objects.filter(id=state_id).exists()

    if state_exist:
        state = State.objects.get(id=state_id)

        if state_slug != slugify(state.name):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            colleges = College.objects.filter(state__id=state_id)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'state_colleges.html', {'colleges': colleges,
                                                   'state': state,
                                                   'slug': state_slug})
