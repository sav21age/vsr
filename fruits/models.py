from django.db import models
from django.urls import reverse
# from django.utils.safestring import mark_safe
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from common.errors import MSG_REQUIRED_BOTH
from common.models import ProductPriceAbstract
from common.validators import SizeValidator
from plants.models import (
    PlantPriceContainer, PlantPriceRootSystem, PlantProductAbstract, PlantSpeciesAbstract)


class FruitSpecies(PlantSpeciesAbstract):
    class Meta(PlantSpeciesAbstract.Meta):
        abstract = False
        verbose_name = 'вид плодовых растений'
        verbose_name_plural = 'виды плодовых растений'


# --

# class FruitProductFlowering(models.Model):
#     CHOICES = (
#         ('E', 'раннее'),
#         ('M', 'среднее'),
#         ('L', 'позднее'),
#     )
#     name = models.CharField('название', max_length=1,
#                             choices=CHOICES, default='E', unique=True,)

#     def __str__(self):
#         return f"{dict(self.CHOICES)[self.name]}"

#     class Meta:
#         ordering = ('name', )
#         verbose_name = 'цветение растения'
#         verbose_name_plural = 'цветение растений'


class FruitProduct(PlantProductAbstract):
    species = models.ForeignKey(
        FruitSpecies, verbose_name='вид', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.', )

    features = models.CharField('особенности', max_length=250, blank=True)

    flowering = models.CharField('цветение', max_length=7, blank=True, )

    self_fertility = models.CharField(
        'самоплодность', max_length=20, blank=True, )

    fruit_ripening = models.CharField(
        'время созревания плодов', max_length=250, blank=True, )

    fruit_taste = models.CharField(
        'вкус плодов', max_length=250, blank=True, )

    fruit_dimension = models.CharField(
        'величина плодов', max_length=7, blank=True, )

    fruit_size = models.CharField(
        'размер плодов, см', max_length=12, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-".',)

    fruit_weight = models.CharField(
        'вес плодов, гр', max_length=12, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-".', )

    fruit_keeping_quality = models.CharField(
        'лежкость плодов', max_length=250, blank=True, )

    beginning_fruiting = models.CharField(
        'начало плодоношения на год', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    search_vector = SearchVectorField(null=True)

    upload_to_dir = 'fruits'

    def get_absolute_url(self):
        return reverse('fruits:detail', kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector",]),
            GinIndex(
                name='trgm_fruitproduct_idx',
                fields=['name'],
                opclasses=['gin_trgm_ops'],
            )
        ]
        ordering = ('name', 'species', )
        verbose_name = 'плодовое растение'
        verbose_name_plural = 'плодовые растения'


# --


class FruitProductPriceAge(models.Model):
    CHOICES = (
        (1, '1-летка'),
        (2, '2-летка'),
        (3, '3-летка'),
        (4, '4-летка'),
        (5, '5-летка'),
        (6, '6-летка'),
        (7, '7-летка'),
        (8, '8-летка'),
        (9, '9-летка'),
        (10, '10-летка'),
        (11, '11-летка'),
        (12, '12-летка'),
        (13, '13-летка'),
        (14, '14-летка'),
        (15, '15-летка'),
        (16, '16-летка'),
        (17, '17-летка'),
    )
    age = models.PositiveSmallIntegerField('возраст', default=1, unique=True,
                                           choices=CHOICES,)

    def __str__(self):
        return f"{dict(self.CHOICES)[self.age]}"

    class Meta:
        ordering = ('age',)
        verbose_name = 'возраст растения'
        verbose_name_plural = 'возраст растений'


class FruitProductPriceRootstock(models.Model):
    CHOICES = (
        (1, 'полукарлик'),
        (2, 'семенной'),
    )
    rootstock = models.PositiveSmallIntegerField('подвой', default=1, unique=True,
                                           choices=CHOICES,)

    def __str__(self):
        return f"{dict(self.CHOICES)[self.rootstock]}"

    class Meta:
        ordering = ('rootstock',)
        verbose_name = 'подвой растения'
        verbose_name_plural = 'подвой растений'


class FruitProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        FruitProduct, verbose_name='растение', related_name='prices', on_delete=models.CASCADE)

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

    rootstock = models.ForeignKey(
        FruitProductPriceRootstock, verbose_name='подвой', blank=True, null=True, on_delete=models.CASCADE)

    age = models.ForeignKey(
        FruitProductPriceAge, verbose_name='возраст', blank=True, null=True, on_delete=models.CASCADE)

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

        s = self.get_complex_name
        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."

    def clean(self):
        if not self.height_from and self.height_to:
            raise ValidationError(
                {'height_from': MSG_REQUIRED_BOTH,
                    'height_to': MSG_REQUIRED_BOTH, },
                code='required')

        if not self.width_from and self.width_to:
            raise ValidationError(
                {'width_from': MSG_REQUIRED_BOTH, 'width_to': MSG_REQUIRED_BOTH, },
                code='required')


        field_list = ('container', 'height_from', 'height_to', 'width_from', 'width_to', 'rs', 'rootstock', 'age',)
        super().validate_one_of_required(field_list)
        super().clean()
