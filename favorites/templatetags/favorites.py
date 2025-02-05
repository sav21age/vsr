from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag(takes_context=True)
def get_favorites(context):

    if not context.get('object'):
        return None

    content_type = ContentType.objects.get_for_model(context['object'])

    if not hasattr(content_type.model_class(), 'favorites'):
        return None

    in_favorites = False
    if context['request'].user.is_authenticated:
        if context['request'].user.favorites_set.filter(content_type=content_type, object_id=context['object'].id):
            in_favorites = True
    # count = Favorites.objects.filter(
    #     content_type=content_type, object_id=context['object'].id).count()
    # return {'in_favorites': in_favorites, 'count': count}
    return in_favorites


# @register.filter
# def toclassname(obj):
#     return obj.__class__.__name__
