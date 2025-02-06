from django import template
from adverts.models import Advert


register = template.Library()


# @register.simple_tag(takes_context=True)
@register.inclusion_tag("adverts/advert.html", takes_context=True)
def get_advert(context):
    request = context['request']
    advert_id = request.COOKIES.get('advert_id')

    try:
        obj = Advert.objects.get()
    except:
        return {
            'show': False,
        }

    if advert_id is not None and obj.id is not None:
        if advert_id == str(obj.id):
            return {
                'show': False,
            }

    return {
        'show': True,
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
    }
