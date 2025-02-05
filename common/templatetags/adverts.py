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
        dct = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body
        }
    except:
        dct = {
            'id': None,
            'title': None,
            'body': None
        }


    if advert_id is not None and dct['id'] is not None:
        if str(dct['id']) == advert_id:
            return None
    
    return {
        'id': dct['id'],
        'title': dct['title'],
        'body': dct['body']
    }
