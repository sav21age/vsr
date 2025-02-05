from django import template
from contacts.models import Contacts

register = template.Library()


# @register.simple_tag()
@register.inclusion_tag("contacts/work_schedule.html")
def get_work_schedule():
    try:
        obj = Contacts.objects.get()
        work_schedule = obj.work_schedule
    except:
        work_schedule = None

    return {
        'work_schedule': work_schedule,
    }
