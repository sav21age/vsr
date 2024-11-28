from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
# from django.contrib.contenttypes import fields
from common.errors import MSG_REQUIRED_BOTH
from common.models import ProductPriceAbstract
from common.validators import SizeUnitValidator, SizeValidator
# from carts.models import CartItem
from plants.models import (
    PlantPlanting, PlantPriceContainer, PlantPriceRootSystem, PlantProductAbstract,
    PlantSpeciesAbstract)


class ConiferSpecies(PlantSpeciesAbstract):
    class Meta(PlantSpeciesAbstract.Meta):
        abstract = False
        verbose_name = 'вид хвойных растений'
        verbose_name_plural = 'виды хвойных растений'


# --


class ConiferProduct(PlantProductAbstract):
    species = models.ForeignKey(
        ConiferSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    features = models.CharField('особенности', max_length=250, blank=True)

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
    
    upload_to_dir = 'conifers'

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
        ConiferProduct, verbose_name='растение', related_name='prices', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.CASCADE)

    # height = models.CharField(
    #     'высота, см', max_length=7, blank=True, validators=(SizeValidator,))

    height_from = models.PositiveSmallIntegerField(
        'высота от, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) = 10+')
    height_to = models.PositiveSmallIntegerField(
        'высота до, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (10) = 10, от (10) и до (20) = 10-20')

    # width = models.CharField(
    #     'ширина, см', max_length=7, blank=True, validators=(SizeValidator,))

    width_from = models.PositiveSmallIntegerField(
        'ширина от, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) = 10+')
    width_to = models.PositiveSmallIntegerField(
        'ширина до, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (10) = 10, от (10) и до (20) = 10-20')

    rs = models.ForeignKey(
        PlantPriceRootSystem, verbose_name='корневая система', blank=True, null=True, on_delete=models.CASCADE)

    shtamb = models.CharField(
        'штамб, см', max_length=7, blank=True, db_index=True, validators=(SizeValidator,),
        help_text='Ветвление на стволе начинается c указанной высоты, см.')

    extra = models.BooleanField(
        'экстра', default=False, db_index=True, help_text='Ухоженные растения.')

    # cart_item = fields.GenericRelation(CartItem)
    
    @property
    def height(self):
        if self.height_from and not self.height_to:
            return f"{self.height_from}+"
        elif self.height_from and self.height_to:
            return f"{self.height_from}-{self.height_to}"
        return None
    
    @property
    def width(self):
        if self.width_from and not self.width_to:
            return f"{self.width_from}+"
        elif self.width_from and self.width_to:
            return f"{self.width_from}-{self.width_to}"
        return None

    def __str__(self):
        # s = ''

        # if self.container:
        #     s = f"{self.container}"

        # if self.height:
        #     s = f"{self.height}" if len(s) == 0 else f"{s} {self.height}"

        # if self.width:
        #     s = f"{self.width}" if len(s) == 0 else f"{s} {self.width}"

        # if self.rs:
        #     s = f"{self.rs}" if len(s) == 0 else f"{s} {self.rs}"

        # if self.shtamb:
        #     field = self._meta.get_field('shtamb')
        #     s = f"{field.verbose_name} {self.shtamb}" if len(
        #         s) == 0 else f"{s} {field.verbose_name} {self.shtamb}"

        # if self.extra:
        #     field = self._meta.get_field('extra')
        #     s = f"{field.verbose_name}" if len(
        #         s) == 0 else f"{s} {field.verbose_name}"

        s = self.get_complex_name
        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."

    def clean(self):
        # if self.height_from and not self.height_to:
        #     raise ValidationError(
        #         {'height_from': MSG_REQUIRED_BOTH, 'height_to': MSG_REQUIRED_BOTH, }, 
        #         code='required')

        if not self.height_from and self.height_to:
            raise ValidationError(
                {'height_from': MSG_REQUIRED_BOTH, 'height_to': MSG_REQUIRED_BOTH, }, 
                code='required')

        # if self.width_from and not self.width_to:
        #     raise ValidationError(
        #         {'width_from': MSG_REQUIRED_BOTH, 'width_to': MSG_REQUIRED_BOTH, }, 
        #         code='required')

        if not self.width_from and self.width_to:
            raise ValidationError(
                {'width_from': MSG_REQUIRED_BOTH, 'width_to': MSG_REQUIRED_BOTH, }, 
                code='required')

        field_list = ('container', 'height_from', 'height_to',
                      'width_from', 'width_to', 'rs', 'shtamb', 'extra',)
        super().validate_one_of_required(field_list)
        super().clean()
