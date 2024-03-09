import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from easy_thumbnails.fields import ThumbnailerImageField
from common.managers import IsVisibleManager


def get_image_path(instance, filename):
    f = os.path.splitext(filename)
    d = 'images'

    if hasattr(instance, 'upload_to_dir'):
        d = f"{d}/{instance.upload_to_dir}"

    if hasattr(instance, 'content_object'):
        if hasattr(instance.content_object, 'upload_to_dir'):
            d = f"{d}/{instance.content_object.upload_to_dir}"

    return f"{d}/{uuid.uuid1().hex}{f[1].lower()}"


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    path = ThumbnailerImageField(
        'Путь к картинке',
        # blank=True,
        max_length=250,
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
