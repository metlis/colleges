from django.http import HttpResponse


def modify_favourites(request):
    params = request.GET

    try:
        session = request.session
    except Exception as e:
        return HttpResponse(e)

    if session.get('favourite_colleges') is None:
        session['favourite_colleges'] = []

    if 'college_id' in params:
        college_id = params['college_id']
        favourite_colleges = session['favourite_colleges']

        if college_id in favourite_colleges:
            favourite_colleges.remove(college_id)
            session['favourite_colleges'] = favourite_colleges
            message = 'Removed'
        else:
            session['favourite_colleges'] = list(set(favourite_colleges + [college_id]))
            message = 'Added'

        return HttpResponse(message)

    response = HttpResponse('No college data')

    response['X-Robots-Tag'] = 'noindex'
    return response