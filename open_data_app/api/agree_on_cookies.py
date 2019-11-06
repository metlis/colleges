from django.http import HttpResponse


def agree_on_cookies(request):

    try:
        session = request.session
    except Exception as e:
        return HttpResponse(e)

    if session.get('cookie_agreement') is None:
        session['cookie_agreement'] = True

    response = HttpResponse('Saved')

    response['X-Robots-Tag'] = 'noindex'
    return response
