import os
from pathlib import Path

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from solo.models import SingletonModel


def get_filepath(instance, filename):
    suffix = Path(filename).suffix
    filepath = f"documents/питомник-растений-вириде-прайс-лист{suffix}"
    fullpath = os.path.join(settings.MEDIA_ROOT, filepath)
    if os.path.exists(fullpath):
        os.remove(fullpath)
    return filepath


class PriceList(SingletonModel):
    file_path = models.FileField(
        'путь к файлу', max_length=150, null=True, blank=True,
        upload_to=get_filepath, validators=(FileExtensionValidator(('xlsx', 'xls', 'pdf', )),)
    )

    file_size = models.PositiveBigIntegerField('размер файла, Б', default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            if self.file_path.path:
                self.file_size = Path(self.file_path.path).stat().st_size
        except:
            pass

        super().save(*args, **kwargs)

    def __str__(self):
        return 'Прайс-лист'
        # if self.file_path:
        #     return f"{self.file_path}"
        # return ''

    def get_absolute_url(self):
        return reverse('price_list_detail')

    class Meta:
        verbose_name = 'загрузить прайс-лист'
        verbose_name_plural = 'загрузить прайс-лист'
