from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector
from django.core.cache import caches
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save

from carts.models import CartItem
from conifers.models import ConiferProduct, ConiferProductPrice
from deciduous.models import DecProduct, DecProductPrice
from fruits.models import FruitProduct, FruitProductPrice
from other.models import OtherProduct, OtherProductPrice
from perennials.models import PerProduct, PerProductPrice
from roses.models import RoseProduct, RoseProductPrice


def receiver_multiple(signal, senders, **kwargs):
    """
    Based on django.dispatch.dispatcher.receiver

    Allows multiple senders so we can avoid using a stack of
    regular receiver decorators with one sender each.
    """

    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender, **kwargs)

        return receiver_func

    return decorator


sender_pages = [ConiferProduct, DecProduct, FruitProduct, PerProduct, 
                OtherProduct, RoseProduct,]

sender_prices = [ConiferProductPrice, DecProductPrice, FruitProductPrice, 
                 PerProductPrice, OtherProductPrice, RoseProductPrice,]


@receiver_multiple([post_save,], senders=sender_pages)
def update_search_vector(sender, instance, created, update_fields, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return
    qs = sender.objects.filter(pk=instance.pk)
    qs.update(search_vector=SearchVector('name', 'name_trans_words', config='russian'))


@receiver_multiple([post_save,], senders=sender_pages)
def remove_hidden_page_cart_items(sender, instance, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return

    if instance.is_visible is False:
        for obj in instance.prices.all():
            content_type = ContentType.objects.get_for_model(obj)
            CartItem.objects.filter(
                content_type_id=content_type.id, object_id=obj.id).delete()


@receiver_multiple([post_delete,], senders=sender_pages)
def remove_deleted_page_cart_items(sender, instance, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return

    for obj in instance.prices.all():
        content_type = ContentType.objects.get_for_model(obj)
        CartItem.objects.filter(
            content_type_id=content_type.id, object_id=obj.id).delete()


@receiver_multiple([post_delete,], senders=sender_prices)
def remove_deleted_price_cart_items(sender, instance, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return
    obj = instance
    content_type = ContentType.objects.get_for_model(obj)
    CartItem.objects.filter(
        content_type_id=content_type.id, object_id=obj.id).delete()


@receiver_multiple([post_save,], senders=sender_pages)
def invalidate_cache(instance, **kwargs):
    if kwargs.get('raw'):  # add for test, pass fixtures
        return

    key = make_template_fragment_key(
        f"{instance._meta.model_name}_detail", [instance.id]
    )
    caches['default'].delete(key)
    # cache.clear()
