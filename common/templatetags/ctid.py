from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()

@register.filter
def toctid(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.id
