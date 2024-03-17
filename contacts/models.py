from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.cache.utils import make_template_fragment_key
from django.dispatch import receiver
from django.core.cache import caches
from common.models import PageAbstract
from solo.models import SingletonModel
from django.core.validators import MinLengthValidator


class Contacts(PageAbstract, SingletonModel):
    company_name = models.CharField('название компании', max_length=80)
    inn = models.CharField('ИНН', max_length=12, blank=True, 
                           validators=[MinLengthValidator(10), ])
    ogrn = models.CharField('ОГРН', max_length=15, blank=True,
                            validators=[MinLengthValidator(13), ])
    kpp = models.CharField('КПП', max_length=9, blank=True,
                           validators=[MinLengthValidator(9), ])

    address = models.CharField(
        'адрес', max_length=200, null=True, blank=True)
    
    phone_retail = models.CharField('телефон (розница)', max_length=20, null=True, blank=True)
    phone_wholesale = models.CharField(
        'телефон (опт)', max_length=20, null=True, blank=True)

    email = models.CharField('email', max_length=50, null=True, blank=True)

    work_schedule = models.CharField(
        'график работы', max_length=50, null=True, blank=True)

    map = models.TextField('карта', null=True, blank=True)

    def __str__(self):
        return 'Контакты'

    class Meta:
        verbose_name = 'контакты'
        verbose_name_plural = 'контакты'

    def get_absolute_url(self):
        return reverse('contacts')


@receiver(post_save, sender=Contacts)
def invalidate_cache(instance, **kwargs):
    if kwargs.get('raw'):  # add for test, pass fixtures
        return

    key = make_template_fragment_key(
        f"{instance._meta.model_name}_detail"
    )
    caches['default'].delete(key)
