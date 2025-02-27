import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.core.files.base import ContentFile
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

    arc_path = models.FileField(
        'путь к заархивированному файлу', max_length=150, null=True, blank=True,
        upload_to=get_filepath,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            if self.file_path:
                path = Path(self.file_path.path)

                arc_path = Path.joinpath(path.parent, f"{path.stem}.zip")
                self.arc_path.save(arc_path, ContentFile(''), save=False)

                with ZipFile(self.arc_path.path, 'w', compression=ZIP_DEFLATED, compresslevel=9) as f:
                    f.write(self.file_path.path, arcname=path.name)
            else:
                self.arc_path.delete()
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
        verbose_name = 'загрузить*'
        verbose_name_plural = 'загрузить'
