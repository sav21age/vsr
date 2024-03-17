from django.db import models
from django.db.models.signals import post_save
from django.core.cache.utils import make_template_fragment_key
from django.dispatch import receiver
from django.core.cache import caches
from common.models import PageAbstract


class Index(PageAbstract):
    description = models.TextField('описание', blank=True)

    con_visible = models.BooleanField('показывать?', default=1,)
    con_name = models.CharField('название', max_length=80, blank=True)
    con_short_description = models.CharField(
        'короткое описание', max_length=250, blank=True)
    con_description = models.TextField('описание', blank=True)

    dec_visible = models.BooleanField('показывать?', default=1,)
    dec_name = models.CharField('название', max_length=80, blank=True)
    dec_short_description = models.CharField(
        'короткое описание', max_length=250, blank=True)
    dec_description = models.TextField('описание', blank=True)

    per_visible = models.BooleanField('показывать?', default=1,)
    per_name = models.CharField('название', max_length=80, blank=True)
    per_short_description = models.CharField(
        'короткое описание', max_length=250, blank=True)
    per_description = models.TextField('описание', blank=True)

    fru_visible = models.BooleanField('показывать?', default=1,)
    fru_name = models.CharField('название', max_length=80, blank=True)
    fru_short_description = models.CharField(
        'короткое описание', max_length=250, blank=True)
    fru_description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'главная страница'
        verbose_name_plural = 'главная страница'


@receiver(post_save, sender=Index)
def invalidate_cache(instance, **kwargs):
    if kwargs.get('raw'):  # add for test, pass fixtures
        return

    key = make_template_fragment_key(
        f"{instance._meta.model_name}_detail"
    )
    caches['default'].delete(key)