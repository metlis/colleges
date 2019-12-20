from open_data_app.models import College

from django.http import HttpResponse
import json


def request_similar_colleges(request):
    college_fields = [f.name for f in College._meta.get_fields()]
    college_fields += ['state__name', 'carnegie__description', 'degree__description', 'level__description',
                       'locale__description', 'ownership__description', 'region__name', 'religion__name']

    favourite_colleges_ids = request.session.get('favourite_colleges')

    similar_colleges = tuple()

    for college_id in favourite_colleges_ids:
        college = College.objects.get(id=college_id)

        filtered_colleges = tuple()

        local_colleges = College.objects.filter(state=college.state).exclude(id__in=favourite_colleges_ids).values(
            *college_fields)
        if len(local_colleges) < 10:
            local_colleges = College.objects.filter(region=college.region).exclude(
                id__in=favourite_colleges_ids).values(*college_fields)

        if college.carnegie:
            same_carnegie_colleges = local_colleges.filter(carnegie=college.carnegie)
            filtered_colleges += tuple(same_carnegie_colleges[0:10])

        if college.religion:
            same_religion_colleges = local_colleges.filter(religion=college.religion)
            filtered_colleges += tuple(same_religion_colleges)

        if len(filtered_colleges) < 10:
            if college.admission_rate:
                similar_admission_colleges = local_colleges.filter(
                    admission_rate__range=(college.admission_rate * 0.8, college.admission_rate * 1.2))
                filtered_colleges += tuple(similar_admission_colleges[0:3])

            if college.in_state_tuition:
                similar_tuition_colleges = local_colleges.filter(
                    in_state_tuition__range=(college.in_state_tuition * 0.8, college.in_state_tuition * 1.2))
                filtered_colleges += tuple(similar_tuition_colleges[0:3])

            if college.completion_rate_four_year_pooled:
                similar_completion_colleges = local_colleges.filter(completion_rate_four_year_pooled__range=(
                    college.completion_rate_four_year_pooled * 0.8, college.completion_rate_four_year_pooled * 1.2))
                filtered_colleges += tuple(similar_completion_colleges[0:3])

        similar_colleges += filtered_colleges

    if len(list(similar_colleges)) > 0:
        dictionary = {}
        for college in similar_colleges:
            if not college['id'] in dictionary:
                dictionary[college['id']] = college

        similar_colleges = [dictionary[key] for key in dictionary]

    response = HttpResponse(
        json.dumps(
            {
                'data': list(similar_colleges)
            }
        ), content_type="application/json")

    response['X-Robots-Tag'] = 'noindex'
    return response
