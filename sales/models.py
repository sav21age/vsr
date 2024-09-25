from urllib.parse import urlsplit, urlunsplit
from django.db import models
from django.contrib.contenttypes import fields
from easy_thumbnails.fields import ThumbnailerImageField
from common.errors import MSG_REQUIRED_BOTH
from common.validators import NumericValidator, PercentValidator
from images.models import Image
from images.models import get_image_path
from django.core.exceptions import ValidationError


class Discount(models.Model):
    date_from = models.DateField('дата начала')
    date_to = models.DateField('дата завершения')

    name = models.CharField(
        'название', max_length=250,
        help_text='Например: Ель канадская Alberta Globe C3')
    
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

    price_old = models.DecimalField('старая цена, руб', max_digits=9, decimal_places=2, blank=True, null=True,)
    price_new = models.DecimalField('новая цена, руб', max_digits=9, decimal_places=2, blank=True, null=True,)

    percent = models.PositiveSmallIntegerField(
        'скидка в процентах', blank=True, null=True, validators=(NumericValidator, PercentValidator))

    images = fields.GenericRelation(Image)
    upload_to_dir = 'discounts'
    
    def __str__(self):
        return f"{self.name}"

    def clean(self):
        url = urlsplit(self.url)
        self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

        if self.percent is not None:
            if self.price_old is not None or self.price_new is not None:
                raise ValidationError(
                    {
                        'price_old': 'Если указана скидка в процентах, то поле должно быть пустым',
                        'price_new': 'Если указана скидка в процентах, то поле должно быть пустым',
                    },
                    code='invalid')

        if self.price_old is None or self.price_new is None:
            if (not self.price_old and self.price_new) or (self.price_old and not self.price_new):
                raise ValidationError(
                    {
                        'price_old': MSG_REQUIRED_BOTH,
                        'price_new': MSG_REQUIRED_BOTH, 
                    },
                    code='required')
        
        if self.price_old is not None and self.price_new is not None:
            if self.price_old <= self.price_new:
                raise ValidationError(
                    {'price_new': 'Новая цена должна быть меньше старой.'},
                    code='required')

        #--

        if self.date_from >= self.date_to:
            raise ValidationError(
                {'date_to': 'Дата завершения должна быть больше даты начала.'},
                code='required')

        super().clean()

    class Meta:
        ordering = ('date_from', 'date_to')
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'
    

class Promotion(models.Model):
    date_from = models.DateField('дата начала')
    date_to = models.DateField('дата завершения')
    name = models.CharField(
        'название', max_length=250,
        help_text='Например: 3 саженца за 1000 рублей')

    description = models.TextField('описание', blank=True)

    images = fields.GenericRelation(Image)
    upload_to_dir = 'promotions'

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.date_from >= self.date_to:
            raise ValidationError(
                {'date_to': 'Дата завершения должна быть больше даты начала.'},
                code='required')
        super().clean()
        
    class Meta:
        ordering = ('date_from', 'date_to')
        verbose_name = 'акция'
        verbose_name_plural = 'акции'


class PromotionItem(models.Model):
    promotion = models.ForeignKey(
        Promotion, verbose_name='акция', on_delete=models.CASCADE)
    
    name = models.CharField(
        'название', max_length=250,
        help_text='Например: Ель канадская Alberta Globe C3')
    url = models.CharField(
        'url-адрес', max_length=250,
        help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/')
    price = models.DecimalField(
        'обычная цена, руб', max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"

    def clean(self):
        url = urlsplit(self.url)
        self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

        super().clean()

    class Meta:
        ordering = ('name',)
        unique_together = (('promotion', 'name'),)
        verbose_name = 'растение'
        verbose_name_plural = 'растения'


# class Discount(models.Model):
#     date_from = models.DateField('дата начала')
#     date_to = models.DateField('дата завершения')

#     name = models.CharField(
#         'название', max_length=250,
#         help_text='Например: Ель канадская Alberta Globe C3')
#     url = models.CharField(
#         'url-адрес', max_length=250, 
#         help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/')

#     description = models.TextField('описание', blank=True)

#     price_old = models.DecimalField('старая цена, руб', max_digits=9, decimal_places=2)
#     price_new = models.DecimalField('новая цена, руб', max_digits=9, decimal_places=2)

#     images = fields.GenericRelation(Image)
#     upload_to_dir = 'discounts'
    
#     type_of = 'discount'

#     def __str__(self):
#         return f"{self.name}"

#     def clean(self):
#         url = urlsplit(self.url)
#         self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

#         super().clean()

#     class Meta:
#         ordering = ('date_from', 'date_to')
#         verbose_name = 'скидка'
#         verbose_name_plural = 'скидки'

#     def get_absolute_url(self):
#         return reverse('discounts')
    

# class Promotion(models.Model):
#     date_from = models.DateField('дата начала')
#     date_to = models.DateField('дата завершения')
#     name = models.CharField(
#         'название', max_length=250,
#         help_text='Например: 3 саженца за 1000 рублей')
#     description = models.TextField('описание', blank=True)

#     images = fields.GenericRelation(Image)
#     upload_to_dir = 'promotions'
#     type_of = 'promotion'

#     def __str__(self):
#         return f"{self.name}"

#     class Meta:
#         ordering = ('date_from', 'date_to')
#         verbose_name = 'акция'
#         verbose_name_plural = 'акции'


# class PromotionItem(models.Model):
#     promotion = models.ForeignKey(
#         Promotion, verbose_name='акция', on_delete=models.CASCADE)
    
#     name = models.CharField(
#         'название', max_length=250,
#         help_text='Например: Ель канадская Alberta Globe C3')
#     url = models.CharField(
#         'url-адрес', max_length=250,
#         help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/')
#     price = models.DecimalField(
#         'обычная цена, руб', max_digits=9, decimal_places=2)

#     def __str__(self):
#         return f"{self.name} {self.price}"

#     def clean(self):
#         url = urlsplit(self.url)
#         self.url = urlunsplit(url._replace(scheme="")._replace(netloc=""))

#         super().clean()

#     class Meta:
#         ordering = ('name',)
#         unique_together = (('promotion', 'name'),)
#         verbose_name = 'растение'
#         verbose_name_plural = 'растения'
