import uuid
from django.db import models
# from django.core.exceptions import ValidationError


class Advert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'заголовок', max_length=120)
    body = models.TextField('текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявление'

    # def save(self, *args, **kwargs):
    #     if not self.pk and self.__class__.objects.exists():
    #         raise ValidationError('Может быть только одно объявление.')
    #         # return None
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
