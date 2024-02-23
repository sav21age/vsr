import re
from django import template

register = template.Library()

@register.filter
def tel(obj):
    return re.sub('[^0-9+]+', '', obj)
