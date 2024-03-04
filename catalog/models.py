from urllib.parse import urlsplit, urlunsplit
from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from images.models import get_image_path


class CatalogItem(models.Model):
    name = models.CharField('название', max_length=250)
    url = models.CharField('url', max_length=250)
    order_number = models.PositiveSmallIntegerField('порядковый номер',)
    image_path = ThumbnailerImageField(
        'Путь к картинке',
        max_length=200,
        upload_to=get_image_path,
        resize_source={'size': (800, 800), 'crop': 'scale'}
    )
    image_title = models.CharField(
        'аттрибут title картинки', max_length=200, blank=True,)

    upload_to_dir = 'catalog'

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        url = urlsplit(self.url)
        self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

        super().clean()

    class Meta:
        ordering = ('order_number',)
        verbose_name = 'элемент'
        verbose_name_plural = 'элементы'

    def get_absolute_url(self):
        return reverse('catalog')
