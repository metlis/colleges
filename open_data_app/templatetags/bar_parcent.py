from django import template

register = template.Library()

def bar_percent(single, aggr):
    try:
        return float(single) / float(aggr) * 100
    except:
        return 0

register.filter('bar_percent', bar_percent)