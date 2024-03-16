from django.db.models.signals import post_save, post_delete
# from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.cache import caches
from django.contrib.postgres.search import SearchVector
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from other.models import OtherProduct
from perennials.models import PerProduct
from roses.models import RoseProduct


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


senders = [ConiferProduct, DecProduct, FruitProduct, PerProduct, OtherProduct, RoseProduct]

@receiver_multiple([post_save,], senders=senders)
def update_search_vector(sender, instance, created, update_fields, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return
    qs = sender.objects.filter(pk=instance.pk)
    qs.update(search_vector=SearchVector('name', config='russian'))


# senders = []
# @receiver_multiple([post_save, post_delete], senders)
# def cache_invalidate(instance, **kwargs):
#     if kwargs.get('raw'):  # add for test, pass fixtures
#         return



@receiver_multiple([post_save,], senders=senders)
def invalidate_cache(instance, **kwargs):
    if kwargs.get('raw'):  # add for test, pass fixtures
        return

    key = make_template_fragment_key(
        f"{instance._meta.model_name}_detail", [instance.id]
    )
    caches['default'].delete(key)
    # cache.clear()
