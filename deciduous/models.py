from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from common.errors import MSG_REQUIRED_BOTH
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

    features = models.CharField('особенности', max_length=250, blank=True)

    leaves = models.CharField('листва', max_length=250, blank=True, )

    crown = models.CharField('крона', max_length=250, blank=True, )

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
        'соцветия', max_length=250, blank=True,)

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

    upload_to_dir = 'deciduous'

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
        DecProduct, verbose_name='растение', related_name='prices', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.CASCADE)

    # height = models.CharField(
    #     'высота, см', max_length=7, blank=True, validators=(SizeValidator,))
    
    height_from = models.PositiveSmallIntegerField(
        'высота от, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20')
    height_to = models.PositiveSmallIntegerField(
        'высота до, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20')
    
    # width = models.CharField(
    #     'ширина, см', max_length=7, blank=True, validators=(SizeValidator,))
    
    width_from = models.PositiveSmallIntegerField(
        'ширина от, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20')
    width_to = models.PositiveSmallIntegerField(
        'ширина до, см', blank=True, null=True, db_index=True,
        help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20')
    
    trunk_diameter = models.CharField(
        'диаметр ствола, см', max_length=7, blank=True, validators=(SizeValidator,))

    rs = models.ForeignKey(
        PlantPriceRootSystem, verbose_name='корневая система', blank=True, null=True, on_delete=models.CASCADE)

    shtamb = models.CharField(
        'штамб, см', max_length=7, blank=True, validators=(SizeValidator,),
        help_text='Ветвление на стволе начинается c указанной высоты, см.')

    extra = models.BooleanField(
        'экстра', default=False, help_text='Ухоженные растения.')

    bush = models.BooleanField(
        'куст', default=False, help_text='Кустовая, многоствольная форма.')

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
        if not self.height_from and self.height_to:
            raise ValidationError(
                {'height_from': MSG_REQUIRED_BOTH, 'height_to': MSG_REQUIRED_BOTH, },
                code='required')

        if not self.width_from and self.width_to:
            raise ValidationError(
                {'width_from': MSG_REQUIRED_BOTH, 'width_to': MSG_REQUIRED_BOTH, },
                code='required')

        field_list = ('container', 'height', 'width', 'trunk_diameter', 'rs', 'shtamb', 'extra',)
        super().validate_one_of_required(field_list)
        super().clean()
