from django.db.models import Avg
from open_data_app.models import College, Template


def _format_int(val):
    rounded_value = round(val)
    formatted_value = '{:,}'.format(rounded_value)
    return formatted_value


def _format_percent(val):
    formatted_value = round(val * 100)
    return formatted_value


def generate_text_main_filter_all():
    # tuition
    public_fees_in_state = College.objects.filter(ownership=1).aggregate(Avg('in_state_tuition'))[
        'in_state_tuition__avg']
    public_fees_out_state = College.objects.filter(ownership=1).aggregate(Avg('out_state_tuition'))[
        'out_state_tuition__avg']
    private_fees_non_profit = College.objects.filter(ownership=2).aggregate(Avg('in_state_tuition'))[
        'in_state_tuition__avg']
    private_fees_for_profit = College.objects.filter(ownership=3).aggregate(Avg('in_state_tuition'))[
        'in_state_tuition__avg']

    # monthly payments
    public_monthly_payments = College.objects.filter(ownership=1).aggregate(Avg('monthly_payments'))[
        'monthly_payments__avg']
    private_monthly_payments_non_profit = College.objects.filter(ownership=2).aggregate(Avg('monthly_payments'))[
        'monthly_payments__avg']
    private_monthly_payments_for_profit = College.objects.filter(ownership=3).aggregate(Avg('monthly_payments'))[
        'monthly_payments__avg']

    # earnings
    public_earnings = College.objects.filter(ownership=1).aggregate(Avg('median_earnings'))[
        'median_earnings__avg']
    private_earnings_non_profit = College.objects.filter(ownership=2).aggregate(Avg('median_earnings'))[
        'median_earnings__avg']
    private_earnings_for_profit = College.objects.filter(ownership=3).aggregate(Avg('median_earnings'))[
        'median_earnings__avg']

    # admission
    admission_public = College.objects.filter(ownership=1).aggregate(Avg('admission_rate'))['admission_rate__avg']
    admission_non_profit = College.objects.filter(ownership=2).aggregate(Avg('admission_rate'))['admission_rate__avg']
    admission_for_profit = College.objects.filter(ownership=3).aggregate(Avg('admission_rate'))['admission_rate__avg']

    # completion
    completion_public = College.objects.filter(ownership=1).aggregate(Avg('completion_rate_four_year_pooled'))[
        'completion_rate_four_year_pooled__avg']
    completion_non_profit = College.objects.filter(ownership=2).aggregate(Avg('completion_rate_four_year_pooled'))[
        'completion_rate_four_year_pooled__avg']
    completion_for_profit = College.objects.filter(ownership=3).aggregate(Avg('completion_rate_four_year_pooled'))[
        'completion_rate_four_year_pooled__avg']

    template = Template.objects.get(name='main_filter_all').content
    text_paragraphs = {}

    for p in template:
        if p == 'College tuition':
            text_paragraphs[p] = template[p].format(_format_int(public_fees_in_state),
                                                    _format_int(public_fees_out_state),
                                                    _format_int(private_fees_non_profit),
                                                    _format_int(private_fees_for_profit))
        if p == 'Monthly payments':
            text_paragraphs[p] = template[p].format(_format_int(public_monthly_payments),
                                                    _format_int(private_monthly_payments_non_profit),
                                                    _format_int(private_monthly_payments_for_profit))
        if p == 'Earnings':
            text_paragraphs[p] = template[p].format(_format_int(public_earnings),
                                                    _format_int(private_earnings_non_profit),
                                                    _format_int(private_earnings_for_profit))
        elif p == 'Admission rate':
            text_paragraphs[p] = template[p].format(_format_percent(admission_public),
                                                    _format_percent(admission_non_profit),
                                                    _format_percent(admission_for_profit))
        elif p == 'Completion rate':
            text_paragraphs[p] = template[p].format(_format_percent(completion_public),
                                                    _format_percent(completion_non_profit),
                                                    _format_percent(completion_for_profit))

    return text_paragraphs
