from django.db import models
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
