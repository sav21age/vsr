from django.db import models
from common.models import PageAbstract


class Index(PageAbstract):
    about_us = models.TextField('о нас')

    class Meta:
        verbose_name = 'главная страница'
        verbose_name_plural = 'главная страница'
