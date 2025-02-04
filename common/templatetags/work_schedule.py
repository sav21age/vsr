from django import template
from contacts.models import Contacts

register = template.Library()


@register.simple_tag()
def get_work_schedule():
    obj = Contacts.objects.get()
    return obj.work_schedule
