from django.core.paginator import Paginator


def handle_pagination(request, colleges):
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    # if parameter page does not have value all, show pagination
    if request.GET.get('page') != 'all':
        paginator = Paginator(colleges, 10)
        colleges = paginator.get_page(page)

    return colleges