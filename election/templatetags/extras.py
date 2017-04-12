from django import template

register = template.Library()

@register.filter(name='result', is_safe=True)
def result(value, all_votes):
    return round(value/all_votes*100, 2)