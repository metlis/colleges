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

    # monthly payments
    p = 'monthly_payments'
    p_avg = 'monthly_payments__avg'
    public_monthly_payments = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    private_monthly_payments_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    private_monthly_payments_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]

    # earnings
    p = 'median_earnings'
    p_avg = 'median_earnings__avg'
    public_earnings = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    private_earnings_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    private_earnings_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]

    # admission
    p = 'admission_rate'
    p_avg = 'admission_rate__avg'
    admission_public = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    admission_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    admission_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]

    # completion
    p = 'completion_rate_four_year_pooled'
    p_avg = 'completion_rate_four_year_pooled__avg'
    completion_public = colleges.filter(ownership=1).aggregate(Avg(p))[p_avg]
    completion_non_profit = colleges.filter(ownership=2).aggregate(Avg(p))[p_avg]
    completion_for_profit = colleges.filter(ownership=3).aggregate(Avg(p))[p_avg]

    template = Template.objects.get(name='main_filter_all').content
    text_paragraphs = {}

    for p in template:
        # general paragraphs for region and state pages
        if p == 'Regional colleges' and region_id:
            text_paragraphs[p] = template[p].format(_format_int(colleges_count),
                                                    region_name,
                                                    _format_int(colleges_public_count),
                                                    _format_int(colleges_private_non_profit),
                                                    _format_int(colleges_private_for_profit))
        if p == 'State colleges' and state_id:
            text_paragraphs[p] = template[p].format(_format_int(colleges_count),
                                                    state_name,
                                                    _format_int(colleges_public_count),
                                                    _format_int(colleges_private_non_profit),
                                                    _format_int(colleges_private_for_profit))

        if p == 'College tuition in the USA' and not region_id and not state_id and not filtered_colleges:
            text_paragraphs[p] = template[p].format(_format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        # tuition paragraphs
        if p == 'College tuition' and filtered_colleges:
            text_paragraphs[p] = template[p].format(_format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        if p == 'College tuition in the region' and region_id:
            text_paragraphs[p] = template[p].format(region_name,
                                                    _format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))

        if p == 'College tuition in the state' and state_id:
            text_paragraphs[p] = template[p].format(state_name,
                                                    _format_amount(public_fees_in_state),
                                                    _format_amount(public_fees_out_state),
                                                    _format_amount(private_fees_non_profit),
                                                    _format_amount(private_fees_for_profit))
        # monthly payments paragraph
        if p == 'Monthly payments':
            text_paragraphs[p] = template[p].format(_format_amount(public_monthly_payments),
                                                    _format_amount(private_monthly_payments_non_profit),
                                                    _format_amount(private_monthly_payments_for_profit))
        # earnings paragraph
        if p == 'Earnings after completion':
            text_paragraphs[p] = template[p].format(_format_amount(public_earnings),
                                                    _format_amount(private_earnings_non_profit),
                                                    _format_amount(private_earnings_for_profit))
        # admission rate paragraph
        elif p == 'Admission rate':
            text_paragraphs[p] = template[p].format(_format_percent(admission_public),
                                                    _format_percent(admission_non_profit),
                                                    _format_percent(admission_for_profit))
        # completion rate paragraph
        elif p == 'Completion rate':
            text_paragraphs[p] = template[p].format(_format_percent(completion_public),
                                                    _format_percent(completion_non_profit),
                                                    _format_percent(completion_for_profit))

    return text_paragraphs
