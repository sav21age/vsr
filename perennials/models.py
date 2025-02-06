from django.db import models
from django.urls import reverse
# from django.core.validators import MinValueValidator
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from common.models import ProductPriceAbstract
from common.validators import FloweringPeriodValidator, NumericValidator, SizeValidator, YearStringValidator
from plants.models import (
    PlantPlanting, PlantPriceContainer, PlantProductAbstract, PlantSpeciesAbstract)


class PerSpecies(PlantSpeciesAbstract):
    class Meta(PlantSpeciesAbstract.Meta):
        abstract = False
        verbose_name = 'вид многолетних растений'
        verbose_name_plural = 'виды многолетних растений'


# --


class PerProductFlowering(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'цветение'
        verbose_name_plural = 'цветение'


class PerProduct(PlantProductAbstract):
    species = models.ForeignKey(
        PerSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    features = models.CharField('особенности', max_length=250, blank=True)

    leaves = models.CharField('листва', max_length=250, blank=True, )

    # flowering = models.CharField('цветение', max_length=250, blank=True, )
    flowering = models.ManyToManyField(
        PerProductFlowering, verbose_name='цветение', related_name='+',
        blank=True,)

    flowering_duration = models.CharField(
        'продолжительность цветения, день', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    flowering_period = models.CharField(
        'период цветения', max_length=9, blank=True,
        validators=(FloweringPeriodValidator,),
        help_text='Можно вводить только римские цифры и "-". Например: IV, IV-VI.', )

    flower_size = models.CharField(
        'размер цветка, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    inflorescence_size = models.CharField(
        'размер соцветия, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    planting = models.ManyToManyField(
        PlantPlanting, verbose_name='место посадки', related_name='+',
        blank=True,)

    shelter_winter = models.CharField(
        'укрытие на зиму', max_length=50, blank=True, )

    winter_zone = models.CharField(
        'зона зимостойкости в градусах', max_length=15, blank=True,)

    search_vector = SearchVectorField(null=True)

    upload_to_dir = 'perennials'

    def get_absolute_url(self):
        return reverse('pers:detail', kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_perproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            )
        ]
        ordering = ('name', 'species', )
        verbose_name = 'многолетнее растение'
        verbose_name_plural = 'многолетние растения'


# --


class PerProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        PerProduct, verbose_name='растение', related_name='prices', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.CASCADE)

    planting_year = models.CharField(
        'год посадки', max_length=4, blank=True, validators=(NumericValidator, YearStringValidator),)

    def __str__(self):
        # s = ''

        # if self.container:
        #     s = f"{self.container}"

        # if self.planting_year:
        #     s = f"{self.planting_year}" if len(
        #         s) == 0 else f"{s} {self.planting_year}"

        s = self.get_complex_name
        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."

    def clean(self):
        field_list = ('container', 'planting_year',)
        super().validate_one_of_required(field_list)
        super().clean()
