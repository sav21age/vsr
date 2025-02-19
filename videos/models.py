import re
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.forms import ValidationError
from common.managers import IsVisibleManager


class Video(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    url = models.URLField('ссылка', max_length=255,
                          help_text='Под видео: "... Еще" -> Экспортировать -> Прямая ссылка. Пример: "https://vk.com/video-111111111_999999999".')
    
    # code = models.TextField('код', validators=[MaxLengthValidator(512)], 
    #                         help_text='Под видео "... Еще" -> Экспортировать -> Код для вставки.')
    
    order_number = models.PositiveSmallIntegerField(
        'порядковый номер', default=0)
    
    is_visible = models.BooleanField('показывать', default=1, db_index=True)

    objects = models.Manager()
    is_visible_objects = IsVisibleManager()

    def __str__(self):
        return f"{self.url}"

    # def save(self, *args, **kwargs):
    #     # url = 'https://vk.com/video-129700322_456239108'
    #     # url = url.replace('https://vk.com/video', '').split('_', 1)

    #     src = re.search(r'src=\"(.*?)\"', self.code)
    #     url = src.group(1)

    #     u = urlparse(url)
    #     query = parse_qs(u.query, keep_blank_values=True)
    #     query.update({'autoplay': 0, 'js_api': 1, 'hd': 2, })
    #     u = u._replace(query=urlencode(query, True))

    #     self.code = self.code.replace(url, urlunparse(u))

    #     w = re.search(r'width=[\"\']([0-9]+)[\"\']', self.code)
    #     if w is not None:
    #         self.code = self.code.replace(w.group(0), 'width="853"')

    #     h = re.search(r'height=[\"\']([0-9]+)[\"\']', self.code)
    #     if h is not None:
    #         self.code = self.code.replace(h.group(0), 'height="480"')

    #     super().save(*args, **kwargs)

    def clean(self):
        # if self.code.find('iframe') == -1:
        #     raise ValidationError(
        #         {'code': 'Не правильный код. Отсутствует тэг iframe.'}
        #     )
        
        # if self.code.find('src') == -1:
        #     raise ValidationError(
        #         {'code': 'Не правильный код. Отсутствует аттрибут src.'}
        #     )

        if self.url.find('clip') >= 0:
            raise ValidationError(
                {'url': 'Нельзя вставлять ВК клипы.'}
            )

        if not re.match(r'((http|https)\:\/\/)?(vk.com|vkvideo.ru)\/video-([0-9]*)_([0-9]*)', self.url):
            raise ValidationError(
                {'url': 'Не правильная ссылка.'}
            )
        
        super().clean()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ('order_number',)
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
