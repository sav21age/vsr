from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.filter
def get_ct_id(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.id
