from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from common.models import ProductPriceAbstract
from common.validators import FloweringPeriodValidator, SizeValidator
from plants.models import (
    PlantPlanting, PlantPriceContainer, PlantPriceRootSystem, PlantProductAbstract, PlantSpeciesAbstract)


class DecSpecies(PlantSpeciesAbstract):
    class Meta(PlantSpeciesAbstract.Meta):
        abstract = False
        verbose_name = 'вид лиственных растений'
        verbose_name_plural = 'виды лиственных растений'


# --


class DecProduct(PlantProductAbstract):
    species = models.ForeignKey(
        DecSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    leaves = models.CharField('листва', max_length=250, blank=True, )

    flowering = models.CharField('цветение', max_length=250, blank=True, )

    flowering_period = models.CharField(
        'период цветения', max_length=7, blank=True,
        validators=(FloweringPeriodValidator,),
        help_text='Можно вводить только римские цифры и "-". Например: IV, IV-VI.', )

    flower_size = models.CharField(
        'размер цветка, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    inflorescence = models.CharField(
        'соцветие', max_length=250, blank=True,)

    inflorescence_size = models.CharField(
        'размер соцветия, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    planting = models.ManyToManyField(
        PlantPlanting, verbose_name='место посадки', related_name='+',
        blank=True,)

    winter_zone = models.CharField(
        'зона зимостойкости в градусах', max_length=15, blank=True,)

    search_vector = SearchVectorField(null=True)

    @property
    def get_min_price(self):
        try:
            return self.decproductprice_set.first().price
        except self.DoesNotExist as e:
            return ''
        except AttributeError as e:
            return ''
        except IndexError as e:
            return ''

    def get_absolute_url(self):
        return reverse('decs:detail', kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_decproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            )
        ]
        ordering = ('name', 'species', )
        verbose_name = 'лиственное растение'
        verbose_name_plural = 'лиственные растения'


# --


class DecProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        DecProduct, verbose_name='растение', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.CASCADE)

    height = models.CharField(
        'высота, см', max_length=7, blank=True, validators=(SizeValidator,))

    width = models.CharField(
        'ширина, см', max_length=7, blank=True, validators=(SizeValidator,))

    rs = models.ForeignKey(
        PlantPriceRootSystem, verbose_name='корневая система', blank=True, null=True, on_delete=models.CASCADE)

    shtamb = models.CharField(
        'штамб, см', max_length=7, blank=True, validators=(SizeValidator,),
        help_text='Ветвление на стволе начинается c указанной высоты, см.')

    extra = models.BooleanField(
        'экстра', default=False, help_text='Ухоженные растения.')

    def __str__(self):
        s = ''

        if self.container:
            s = f"{self.container}"

        if self.height:
            s = f"{self.height}" if len(s) == 0 else f"{s} {self.height}"

        if self.width:
            s = f"{self.width}" if len(s) == 0 else f"{s} {self.width}"

        if self.rs:
            s = f"{self.rs}" if len(s) == 0 else f"{s} {self.rs}"

        if self.shtamb:
            field = self._meta.get_field('shtamb')
            s = f"{field.verbose_name} {self.shtamb}" if len(
                s) == 0 else f"{s} {field.verbose_name} {self.shtamb}"

        if self.extra:
            field = self._meta.get_field('extra')
            s = f"{field.verbose_name}" if len(
                s) == 0 else f"{s} {field.verbose_name}"

        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."