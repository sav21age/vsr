from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from common.models import ProductAbstract, ProductPriceAbstract


class OtherProductCategory(models.Model):
    CHOICES = (
        ('BOOK', 'Книги'),
        ('RELATED', 'Сопутствующие товары'),
    )

    name = models.CharField('название', max_length=7,
                            choices=CHOICES, default='FRU', unique=True,)

    def __str__(self):
        return f"{dict(self.CHOICES)[self.name]}"

    class Meta:
        ordering = ('name', )
        verbose_name = 'категория товара'
        verbose_name_plural = 'категории товаров'


class OtherProduct(ProductAbstract):
    category = models.ForeignKey(
        OtherProductCategory, verbose_name='категория товара', on_delete=models.CASCADE,)
    
    search_vector = SearchVectorField(null=True)

    upload_to_dir = 'other'

    def get_absolute_url(self):
        return reverse(f"{self.category.name.lower()}_detail", kwargs={"slug": self.slug})

    @property
    def get_min_price(self):
        try:
            return self.otherproductprice_set.first().price
        except self.DoesNotExist:
            return ''
        except AttributeError:
            return ''
        except IndexError:
            return ''

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_otherproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            )    
        ]
        ordering = ('category', 'name', )
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class OtherProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        OtherProduct, verbose_name='товар', on_delete=models.CASCADE)

    property = models.CharField(
        'параметры', max_length=150,)

    def __str__(self):
        # s = ''

        # if self.property:
        #     s = f"{self.property}"
        
        s = self.get_complex_name
        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."
