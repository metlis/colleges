from django.db.models import Avg
from open_data_app.models import College, Template, Region, State


def _format_int(val):
    if val is None:
        return 'not known'
    rounded_value = round(val)
    return '{:,}'.format(rounded_value)


def _format_amount(val):
    if val is None:
        return 'not known'
    rounded_value = round(val)
    return '{:,}$'.format(rounded_value)


def _format_percent(val):
    if val is None:
        return 'not known'
    rounded_value = round(val * 100)
    return '{}%'.format(rounded_value)


def generate_filter_text(region_id='', state_id='', filtered_colleges=''):
    if filtered_colleges:
        colleges = filtered_colleges
    else:
        colleges = College.objects.all()

    # region data
    if region_id:
        region = Region.objects.get(id=region_id)
        region_name, region_slug, region_states = region.get_parsed_names()
        colleges = colleges.filter(region=region)

    # state data
    if state_id:
        state = State.objects.get(id=state_id)
        state_name = state.name
        colleges = colleges.filter(state=state)

    #  general
    colleges_count = colleges.count()
    colleges_public_count = colleges.filter(ownership=1).count()
    colleges_private_non_profit = colleges.filter(ownership=2).count()
    colleges_private_for_profit = colleges.filter(ownership=3).count()

    # tuition
    p = 'in_state_tuition'
    p_avg = 'in_state_tuition__avg'
    public_fees_in_state = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    public_fees_out_state = colleges.filter(ownership=1).aggregate(Avg('out_state_tuition'))['out_state_tuition__avg']
    private_fees_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    private_fees_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]
    none_fees_data = public_fees_in_state is None and public_fees_out_state is None \
                     and private_fees_non_profit is None and private_fees_for_profit is None

    # monthly payments
    p = 'monthly_payments'
    p_avg = 'monthly_payments__avg'
    public_monthly_payments = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    private_monthly_payments_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    private_monthly_payments_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]
    none_monthly_payments_data = public_monthly_payments is None and private_monthly_payments_non_profit is None \
                                 and private_monthly_payments_for_profit is None

    # earnings
    p = 'median_earnings'
    p_avg = 'median_earnings__avg'
    public_earnings = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    private_earnings_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    private_earnings_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]
    none_earnings_data = public_earnings is None and private_earnings_non_profit is None \
                         and private_earnings_for_profit is None

    # admission
    p = 'admission_rate'
    p_avg = 'admission_rate__avg'
    admission_public = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    admission_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    admission_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]
    none_admission_data = admission_public is None and admission_non_profit is None and admission_for_profit is None

    # completion
    p = 'completion_rate_four_year_pooled'
    p_avg = 'completion_rate_four_year_pooled__avg'
    completion_public = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    completion_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    completion_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]
    none_completion_data = completion_public is None and completion_non_profit is None and completion_for_profit is None

    template = Template.objects.get(name='main_filter_all').content
    text_paragraphs = {}

    for p in template:
        # general paragraph for the main filter page
        if p == 'US colleges distribution by ownership' \
                and not region_id \
                and not state_id \
                and not filtered_colleges:
            text_paragraphs[p] = template[p].format(_format_int(colleges_count),
                                                    _format_int(colleges_public_count),
                                                    _format_int(colleges_private_non_profit),
                                                    _format_int(colleges_private_for_profit))
        # general paragraph for region pages
        if p == 'Colleges in {} region' and region_id:
            text_paragraphs[p.format(region_name)] = template[p].format(_format_int(colleges_count),
                                                                        region_name,
                                                                        _format_int(colleges_public_count),
                                                                        _format_int(colleges_private_non_profit),
                                                                        _format_int(colleges_private_for_profit))
        # general paragraph for state pages
        if p == 'State colleges in {}' and state_id:
            text_paragraphs[p.format(state_name)] = template[p].format(_format_int(colleges_count),
                                                                       state_name,
                                                                       _format_int(colleges_public_count),
                                                                       _format_int(colleges_private_non_profit),
                                                                       _format_int(colleges_private_for_profit))

        # tuition paragraph for the main filter page
        if p == 'College tuition in the USA' \
                and not region_id \
                and not state_id \
                and not filtered_colleges \
                and not none_fees_data:
            text_paragraphs[p] = template[p].format(_format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        # tuition paragraph for filter pages with no geo titles
        if p == 'College tuition' and filtered_colleges and not none_fees_data:
            text_paragraphs[p] = template[p].format(_format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        # tuition paragraph for filter pages with region filter as the only filter
        if p == 'College tuition in the region' and region_id and not none_fees_data:
            text_paragraphs[p] = template[p].format(region_name,
                                                    _format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        # tuition paragraph for filter pages with state filter as the only filter
        if p == 'College tuition in the state' and state_id and not none_fees_data:
            text_paragraphs[p] = template[p].format(state_name,
                                                    _format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))
        # monthly payments paragraph
        if p == 'Monthly payments' and not none_monthly_payments_data:
            text_paragraphs[p] = template[p].format(_format_amount(public_monthly_payments),
                                                    _format_amount(private_monthly_payments_non_profit),
                                                    _format_amount(private_monthly_payments_for_profit))
        # earnings paragraph
        if p == 'Earnings after completion' and not none_earnings_data:
            text_paragraphs[p] = template[p].format(_format_amount(public_earnings),
                                                    _format_amount(private_earnings_non_profit),
                                                    _format_amount(private_earnings_for_profit))
        # admission rate paragraph
        elif p == 'Admission rate' and not none_admission_data:
            text_paragraphs[p] = template[p].format(_format_percent(admission_public),
                                                    _format_percent(admission_non_profit),
                                                    _format_percent(admission_for_profit))
        # completion rate paragraph
        elif p == 'Completion rate' and not none_completion_data:
            text_paragraphs[p] = template[p].format(_format_percent(completion_public),
                                                    _format_percent(completion_non_profit),
                                                    _format_percent(completion_for_profit))

    return text_paragraphs
