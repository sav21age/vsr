import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.managers import IsVisibleManager
from easy_thumbnails.fields import ThumbnailerImageField


def get_image_path(instance, filename):
    f = os.path.splitext(filename)
    dir = 'images'
    if hasattr(instance, 'upload_to_dir'):
        dir = '{0}/{1}'.format(dir, instance.upload_to_dir)
    return '{0}/{1}{2}'.format(dir, uuid.uuid1().hex, f[1].lower())


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    path = ThumbnailerImageField(
        'Путь к картинке',
        blank=True,
        max_length=200,
        upload_to=get_image_path,
        resize_source={'size': (800, 800), 'crop': 'scale'}
    )

    # alt = models.CharField('аттрибут alt', max_length=200, null=True, blank=True, )
    title = models.CharField(
        'аттрибут title', max_length=200, blank=True,)
    order_number = models.PositiveSmallIntegerField(
        'порядковый номер', default=0)
    is_visible = models.BooleanField('показывать', default=1, db_index=True)

    objects = models.Manager()
    is_visible_objects = IsVisibleManager()

    def __str__(self):
        return f"{self.path.path}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ('order_number',)
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'
