from django.db import models
from common.managers import IsVisibleManager
from django.contrib.contenttypes import fields
from favorites.models import Favorites
from images.models import Image
from common.managers import SearchManager


class PageAbstract(models.Model):
    head_title = models.CharField('заголовок', max_length=80)
    meta_description = models.CharField('мета описание', max_length=160)

    name = models.CharField('название', max_length=80, unique=True)
    slug = models.SlugField('слаг',
                            max_length=80, blank=False, unique=True)

    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    is_visible = models.BooleanField('показывать?', default=1, db_index=True)

    objects = models.Manager()
    
    is_visible_objects = IsVisibleManager()

    def __str__(self):
        return str(self.name)
    
    class Meta:
        abstract = True


class ProductAbstract(PageAbstract):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_description = models.CharField('короткое описание', max_length=250)
    description = models.TextField('описание', blank=True)
    
    images = fields.GenericRelation(Image)
    favorites = fields.GenericRelation(Favorites)

    objects = SearchManager()

    @property
    def get_image(self):
        try:
            # return self.images.order_by('order_number').first()
            return self.images.first()
        except self.DoesNotExist:
            return ''
        except IndexError:
            return ''

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True


class ProductPriceAbstract(models.Model):
    price = models.DecimalField('цена, руб', max_digits=9, decimal_places=2)

    class Meta:
        abstract = True
        ordering = ('price',)
        verbose_name = 'цена'
        verbose_name_plural = 'цены'