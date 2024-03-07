from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
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

    rootstock = models.CharField('подвой', max_length=15, blank=True, )

    fruit_ripening = models.CharField(
        'время созревания плодов', max_length=250, blank=True, )

    fruit_taste = models.CharField(
        'вкус плодов', max_length=250, blank=True, )

    fruit_size = models.CharField(
        'размер плодов, см', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    fruit_keeping_quality = models.CharField(
        'лежкость плодов', max_length=250, blank=True, )

    beginning_fruiting = models.CharField(
        'начало плодоношения у растения, г', max_length=7, blank=True,
        validators=(SizeValidator,),
        help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )

    search_vector = SearchVectorField(null=True)

    @property
    def get_min_price(self):
        try:
            return self.fruitproductprice_set.first().price
        except self.DoesNotExist as e:
            return ''
        except AttributeError as e:
            return ''
        except IndexError as e:
            return ''

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
    )
    age = models.PositiveSmallIntegerField('возраст', default=1, unique=True,
                                           choices=CHOICES,)

    def __str__(self):
        return f"{dict(self.CHOICES)[self.age]}"

    class Meta:
        ordering = ('age',)
        verbose_name = 'возраст растения'
        verbose_name_plural = 'возраст растений'


class FruitProductPrice(ProductPriceAbstract):
    product = models.ForeignKey(
        FruitProduct, verbose_name='растение', on_delete=models.CASCADE)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.CASCADE)

    height = models.CharField(
        'высота, см', max_length=7, blank=True, validators=(SizeValidator,))

    width = models.CharField(
        'ширина, см', max_length=7, blank=True, validators=(SizeValidator,))

    rs = models.ForeignKey(
        PlantPriceRootSystem, verbose_name='корневая система', blank=True, null=True, on_delete=models.CASCADE)

    age = models.ForeignKey(
        FruitProductPriceAge, verbose_name='возраст', blank=True, null=True, on_delete=models.CASCADE)

    # CHOICES = (
    #     ('1-летка','1-летка'),
    #     ('2-летка','2-летка'),
    #     ('3-летка','3-летка'),
    #     ('4-летка','4-летка'),
    #     ('5-летка','5-летка'),
    #     ('6-летка','6-летка'),
    #     ('7-летка','7-летка'),
    #     ('8-летка','8-летка'),
    #     ('9-летка','9-летка'),
    # )
    # age = models.CharField('возраст', max_length=7, choices=CHOICES,
    #                              blank=True, default='',)

    # shtamb = models.CharField(
    #     'штамб', max_length=7, blank=True, validators=(SizeValidator,),
    #     help_text='Ветвление на стволе начинается c указанной высоты.')

    # extra = models.BooleanField(
    #     'экстра', default=False, help_text='Ухоженные растения.')

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

        # if self.shtamb:
        #     field = self._meta.get_field('shtamb')
        #     s = f"{field.verbose_name} {self.shtamb}" if len(
        #         s) == 0 else f"{s} {field.verbose_name} {self.shtamb}"

        # if self.extra:
        #     field = self._meta.get_field('extra')
        #     s = f"{field.verbose_name}" if len(
        #         s) == 0 else f"{s} {field.verbose_name}"

        return f"{self.price}" if len(s) == 0 else f"{s} ={self.price} руб."
