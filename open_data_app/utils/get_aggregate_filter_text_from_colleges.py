from open_data_app.utils.text_generators import generate_filter_text


def get_aggregate_filter_text_from_colleges(request, colleges, region_id='', state_id=''):
    aggregate_text = ''

    params = request.GET
    if len(params) == 0 and colleges.count() > 1:
        aggregate_text = generate_filter_text(region_id, state_id, colleges)

    return aggregate_text
