from urllib.parse import urlsplit, urlunsplit
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from common.managers import IsVisibleManager
from images.models import get_image_path
from plants.models import PlantDivision


class Seedling(models.Model):
    is_visible = models.BooleanField('показывать?', default=1, db_index=True)

    name = models.CharField('название', max_length=80, unique=True)

    division = models.ForeignKey(
        PlantDivision, verbose_name='отдел', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел. Пример: Хвойные.',)

    url = models.CharField(
        'url-адрес', max_length=250,
        help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/')

    image_path = ThumbnailerImageField(
        'Путь к картинке',
        max_length=200,
        upload_to=get_image_path,
        resize_source={'size': (800, 800), 'crop': 'scale'}
    )

    image_title = models.CharField(
        'аттрибут title картинки', max_length=200, blank=True,)

    upload_to_dir = 'seedlings'

    date_shooting = models.DateField('дата съемки')

    objects = models.Manager()

    is_visible_objects = IsVisibleManager()

    def __str__(self):
        return str(self.name)

    def clean(self):
        url = urlsplit(self.url)
        self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

    class Meta:
        ordering = ('name', )
        unique_together = (('name', 'division'),)
        verbose_name = 'саженцы'
        verbose_name_plural = 'саженцы'
