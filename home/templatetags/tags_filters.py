from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, split_by):
    if value == '':
        return None
    return value.split(split_by)