from django import template
from contacts.models import WorkSchedule

register = template.Library()


# @register.simple_tag()
@register.inclusion_tag("contacts/work_schedule.html")
def get_work_schedule():
    try:
        obj = WorkSchedule.objects.get()
        name = obj.name
    except:
        name = None

    return {
        'name': name,
    }
