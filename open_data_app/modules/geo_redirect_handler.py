from open_data_app.models import Region, State

from django.http import Http404, HttpResponsePermanentRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


def handle_geo_redirect(geo_name, geo_id, slug, param_name='', param_value=''):
    try:
        if geo_name == 'region':
            region = Region.objects.get(id=geo_id)
            if slug != region.slug:
                raise Http404()
        else:
            state = State.objects.get(id=geo_id)
            if slug != state.slug:
                raise Http404()

        if not param_name and not param_value:
            return HttpResponsePermanentRedirect(reverse('college_app:{}'.format(geo_name), kwargs={
                '{}_slug'.format(geo_name): slug,
            }))
        else:
            return HttpResponsePermanentRedirect(reverse('college_app:{}_param'.format(geo_name), kwargs={
                '{}_slug'.format(geo_name): slug,
                'param_name': param_name,
                'param_value': param_value,
            }))
    except ObjectDoesNotExist:
        raise Http404()