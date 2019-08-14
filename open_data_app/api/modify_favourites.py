from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse


def modify_favourites(request):
    params = request.GET
    session = Session.objects.get(session_key=params['session_key'])
    session_data = session.get_decoded()

    if session_data.get('favourite_colleges') is None:
        session_data['favourite_colleges'] = []

    if params['college_id']:
        if params['college_id'] in session_data['favourite_colleges']:
            session_data['favourite_colleges'].remove(params['college_id'])
            session.session_data = SessionStore().encode(session_data)
            session.save()
            return HttpResponse('Removed')
        else:
            session_data['favourite_colleges'] = list(set(request.session['favourite_colleges'] + [params['college_id']]))
            session.session_data = SessionStore().encode(session_data)
            session.save()
            return HttpResponse('Added')

    return HttpResponse('No college data')