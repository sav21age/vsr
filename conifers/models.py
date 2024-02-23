from django.db import models
from django.urls import reverse
from carts.models import CartItem
from common.models import ProductPriceAbstract
from plants.models import (
    PlantPlanting, PlantPriceContainer, PlantPriceRootSystem, PlantProductAbstract,
    PlantSpeciesAbstract)
from common.validators import SizeUnitValidator, SizeValidator
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.contenttypes import fields


class ConiferSpecies(PlantSpeciesAbstract):
    class Meta:
        verbose_name = 'вид хвойных растений'
        verbose_name_plural = 'виды хвойных растений'


# --


class ConiferProduct(PlantProductAbstract):
    species = models.ForeignKey(
        ConiferSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    needles = models.CharField('хвоя', max_length=250, blank=True, )

    height10 = models.CharField(
        'высота в 10 лет', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-" и ","', )

    width10 = models.CharField(
        'ширина в 10 лет', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-" и ","', )

    height1 = models.CharField(
        'годовой прирост в высоту', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-" и ","', )

    width1 = models.CharField(
        'годовой прирост в ширину', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-" и ","', )

    planting = models.ManyToManyField(
        PlantPlanting, verbose_name='место посадки', related_name='+',
        blank=True,)

    shelter = models.CharField(
        'укрытие', max_length=50, blank=True, )

    winter_zone = models.CharField(
        'зона зимостойкости в градусах', max_length=30, blank=True,)

    search_vector = SearchVectorField(null=True)

    @property
    def get_min_price(self):
        try:
            return self.coniferproductprice_set.first().price
        except self.DoesNotExist as e:
            return ''
        except AttributeError as e:
            return ''
        except IndexError as e:
            return ''

    def get_absolute_url(self):
        return reverse('conifers:detail', kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_coniferproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            ),
            ]
        # indexes = [GinIndex(SearchVector(
        #     'name', config="russian"), name="search_vector_idx",),]
        # indexes = [
        #     GinIndex(
        #         name='vector_coniferproduct_idx',
        #         fields=['name'], 
        #         opclasses=['gin_trgm_ops'],
        #     )
        # ]
        ordering = ('name', 'species', )
        verbose_name = 'хвойное растение'
        verbose_name_plural = 'хвойные растения'


# --


class ConiferProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        ConiferProduct, verbose_name='растение', on_delete=models.CASCADE)

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

    cart_item = fields.GenericRelation(CartItem)

    # tt = models.ForeignKey(
    #     PlantPriceTrunkDiameter, verbose_name='диаметр ствола', blank=True, null=True, on_delete=models.CASCADE)

    # width = models.ForeignKey(
    #     PlantPriceWidth, verbose_name='ширина', blank=True, null=True, on_delete=models.CASCADE)

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
            s = f"{field.verbose_name}" if len(s) == 0 else f"{s} {field.verbose_name}"

        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."


# class ConiferProductHeight(PlantHeightAbstract):
#     pass

# class ConiferProductWidth(PlantWidthAbstract):
#     pass
