from django.db import models
from django.urls import reverse
from common.models import ProductPriceAbstract
from common.validators import SizeValidator
from plants.models import (
    PlantPriceContainer, PlantProductAbstract)
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField


class RoseSpecies(models.Model):
    name = models.CharField(
        'название', max_length=100, unique=True,
        help_text='Классификация роз: Вид. Пример: Роза канадская.',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('name', )
        verbose_name = 'вид розы'
        verbose_name_plural = 'виды роз'


# --

class RoseProduct(PlantProductAbstract):
    species = models.ForeignKey(
        RoseSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    flowering = models.CharField('цветение', max_length=100, blank=True, )

    quantity_on_stem = models.CharField(
        'количество на стебле', max_length=5, blank=True, null=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, "-" и "+"', )

    flavor = models.CharField('аромат', max_length=15, blank=True, )

    flower_size = models.CharField(
        'размер цветка, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    resistance_fungus = models.CharField(
        'устойчивость к грибковым инфекциям', max_length=15, blank=True, )

    resistance_rain = models.CharField(
        'устойчивость к дождю', max_length=15, blank=True, )

    shelter_winter = models.CharField(
        'укрытие на зиму', max_length=50, blank=True, )
    
    winter_zone = models.CharField(
        'зона зимостойкости в градусах', max_length=15, blank=True,)


    search_vector = SearchVectorField(null=True)

    upload_to_dir = 'roses'

    @property
    def get_min_price(self):
        try:
            return self.roseproductprice_set.first().price
        except self.DoesNotExist as e:
            return ''
        except AttributeError as e:
            return ''
        except IndexError as e:
            return ''

    def get_absolute_url(self):
        return reverse('roses:detail', kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_roseproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            )
        ]
        ordering = ('name', 'species', )
        verbose_name = 'роза'
        verbose_name_plural = 'розы'


# --


class RoseProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        RoseProduct, verbose_name='роза', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', on_delete=models.CASCADE)

    def __str__(self):
        # s = ''

        # if self.container:
        #     s = f"{self.container}"
        
        s = self.get_complex_name
        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."
