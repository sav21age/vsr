import os
from pathlib import Path
from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from solo.models import SingletonModel


def get_filepath(instance, filename):
    suffix = Path(filename).suffix
    filepath = f"documents/price-list-viride{suffix}"
    fullpath = os.path.join(settings.MEDIA_ROOT, filepath)
    if os.path.exists(fullpath):
        os.remove(fullpath)
    return filepath


class PriceList(SingletonModel):
    file_path = models.FileField(
        'путь к файлу', upload_to=get_filepath, max_length=140,
        validators=(FileExtensionValidator(('xlsx',)),)
    )

    def __str__(self):
        if self.file_path:
            return f"{self.file_path.url}"
        return ''

    class Meta:
        verbose_name = 'загрузить прайс-лист'
        verbose_name_plural = 'загрузить прайс-лист'
