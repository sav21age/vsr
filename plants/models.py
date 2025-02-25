from django.db import models
from common.models import ProductAbstract
from common.validators import SizeUnitValidator


class PlantDivision(models.Model):
    CHOICES = (
        ('FRU', 'Плодовые'),
        ('DEC', 'Лиственные'),
        ('PER', 'Mноголетние'),
        ('CON', 'Хвойные'),
    )
    name = models.CharField('название', max_length=3,
                            choices=CHOICES, default='FRU', unique=True,)

    def __str__(self):
        return f"{dict(self.CHOICES)[self.name]}"

    class Meta:
        ordering = ('name', )
        verbose_name = 'отдел растений'
        verbose_name_plural = 'отделы растений'


class PlantGenus(models.Model):
    division = models.ForeignKey(
        PlantDivision, verbose_name='отдел', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел. Пример: Хвойные.',)
    name = models.CharField(
        'род', max_length=100,
        help_text='Классификация растений: Отдел \ Род. Пример: Хвойные \ Ель.',)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name', )
        unique_together = (('name', 'division'),)
        verbose_name = 'род растений'
        verbose_name_plural = 'рода растений'


class PlantSpeciesAbstract(models.Model):
    genus = models.ForeignKey(
        PlantGenus, verbose_name='род', on_delete=models.CASCADE,
        help_text='Классификация растений: Отдел \ Род. Пример: Хвойные \ Ель.',
    )
    name = models.CharField(
        'вид', max_length=100, unique=True,
        help_text='Классификация растений: Отдел \ Род \ Вид. Пример: Хвойные \ Ель \ Ель канадская.',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True
        ordering = ('name', )
        # unique_together = (('name', 'genus'),)

# --


class PlantAdvantage(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'достоинства'
        verbose_name_plural = 'достоинства'


class PlantPlanting(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'место посадки'
        verbose_name_plural = 'место посадки'


class PlantProductAbstract(ProductAbstract):
    scientific_name = models.CharField(
        'научное название', max_length=100, blank=True, )

    advantages = models.ManyToManyField(
        PlantAdvantage, verbose_name='достоинства', related_name='+',
        blank=True,)
    
    height = models.CharField(
        'высота взрослого растения', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-" и ",". Например: 0,5 м, 0,5-1 м, от 0,5 м, до 0,5 м', )

    width = models.CharField(
        'ширина взрослого растения', max_length=10, blank=True,
        validators=(SizeUnitValidator,),
        help_text='Можно вводить цифры, от, до, м, см, "-"  и ",". Например: 0,5 м, 0,5-1 м, от 0,5 м, до 0,5 м', )
    
    @property
    def get_min_price(self):
        try:
            if self.prices.count() > 1 and self.prices.first().price == 0:
                return self.prices.filter(price__gt=0).first().price
            return self.prices.first().price
        except self.DoesNotExist:
            return None
        except:
            return None
        
    class Meta:
        abstract = True


# --


class PlantPriceContainer(models.Model):
    name = models.CharField('название', max_length=5, unique=True,)
    description = models.CharField('описание', max_length=200,
        help_text='Например: Горшок объемом 10 литров.')
    order_number = models.DecimalField(
        'порядковый номер', max_digits=5, decimal_places=2, blank=True, null=True,
        help_text='Например: P9-0.9, P15-0.15, C1-1, C10-10 и т.д.')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('order_number', )
        verbose_name = 'контейнер'
        verbose_name_plural = 'контейнеры'


class PlantPriceRootSystem(models.Model):
    abbr = models.CharField('аббревиатура', max_length=10)
    abbr_en = models.CharField(
        'аббревиатура на английском', max_length=10, blank=True, )
    description = models.TextField('описание',)

    def __str__(self):
        return f"{self.abbr}"

    class Meta:
        ordering = ('abbr', )
        verbose_name = 'корневая система'
        verbose_name_plural = 'корневые системы'


#--


# class PlantPriceHeightAbstract(models.Model):
#     h_from = models.IntegerField('высота, от', )
#     h_to = models.IntegerField('высота, до', blank=True, null=True, )

#     def __str__(self):
#         if not self.h_to:
#             return f"{self.h_from}+"

#         return f"{self.h_from}-{self.h_to}"
    
#     def validate_unique(self, exclude=None):
#         model = self._meta.model
#         if not self.h_to and model.objects.exclude(id=self.id) \
#                 .filter(h_from=self.h_from, h_to__isnull=True).exists():
#             raise ValidationError(
#                 {'h_from': msg_already_exists}, code='invalid')

#         super().validate_unique(exclude)

#     class Meta:
#         abstract = True
#         ordering = ('h_from', 'h_to', )
#         unique_together = (('h_from', 'h_to'),)
#         verbose_name = 'высота'
#         verbose_name_plural = 'высота'

# --

# class PlantSizeUnits(models.Model):
#     CHOICES = (
#         ('CM', 'см'),
#         ('M', 'м'),
#     )
#     name = models.CharField('название', max_length=2,
#                             choices=CHOICES, default='CM', unique=True,)

#     def __str__(self):
#         return f"{dict(self.CHOICES)[self.name]}"

#     class Meta:
#         ordering = ('name', )
#         verbose_name = 'единица измерения'
#         verbose_name_plural = 'единицы измерения'


# class PlantHeightAbstract(models.Model):
#     h_from = models.DecimalField(
#         'высота, от', max_digits=4, decimal_places=1, blank=True, null=True, )
#     h_to = models.DecimalField(
#         'высота, до', max_digits=4, decimal_places=1, blank=True, null=True, )
#     units = models.ForeignKey(
#         PlantSizeUnits, verbose_name='единицы измерения', on_delete=models.CASCADE)

#     def __str__(self):
#         # h_from = f"{self.h_from.normalize()}"
#         # h_to = f"{self.h_to.normalize()}"
#         h_from = f"{self.h_from}"
#         h_to = f"{self.h_to}"
#         if self.units.name == 'СМ':
#             if self.h_from:
#                 h_from = f"{self.h_from:.0f}"
#             if self.h_to:
#                 h_to = f"{self.h_to:.0f}"

#         if not self.h_to:
#             return f"от {h_from} {self.units}"

#         if not self.h_from:
#             return f"до {h_to} {self.units}"

#         return f"{h_from}-{h_to} {self.units}"

#     def clean(self):
#         if not self.h_from and not self.h_to:
#             raise ValidationError(
#                 {'h_from': msg_required, 'h_to': msg_required}, code='required')

#         super().clean()

#     def validate_unique(self, exclude=None):
#         model = self._meta.model
#         if not self.h_to and model.objects.exclude(id=self.id) \
#                 .filter(h_from=self.h_from, units=self.units, h_to__isnull=True).exists():
#             raise ValidationError(
#                 {'h_from': msg_already_exists, 'units': msg_already_exists}, code='invalid')

#         if not self.h_from and model.objects.exclude(id=self.id) \
#                 .filter(h_to=self.h_to, units=self.units, h_from__isnull=True).exists():
#             raise ValidationError(
#                 {'h_to': msg_already_exists, 'units': msg_already_exists}, code='invalid')

#         super().validate_unique(exclude)

#     class Meta:
#         abstract = True
#         ordering = ('h_from', 'h_to', )
#         unique_together = (('h_from', 'h_to', 'units'), )
#         verbose_name = 'высота взрослого растения'
#         verbose_name_plural = 'высота взрослых растений'


# class PlantWidthAbstract(models.Model):
#     w_from = models.DecimalField(
#         'ширина, от', max_digits=4, decimal_places=1, blank=True, null=True, )
#     w_to = models.DecimalField(
#         'ширина, до', max_digits=4, decimal_places=1, blank=True, null=True, )
#     units = models.ForeignKey(
#         PlantSizeUnits, verbose_name='единицы измерения', on_delete=models.CASCADE)

#     def __str__(self):
#         w_from = f"{self.w_from}"
#         w_to = f"{self.w_to}"
#         if self.units.name == 'СМ':
#             if self.w_from:
#                 w_from = f"{self.w_from:.0f}"
#             if self.w_to:
#                 w_to = f"{self.w_to:.0f}"

#         if not self.w_to:
#             return f"от {w_from} {self.units}"

#         if not self.w_from:
#             return f"до {w_to} {self.units}"

#         return f"{w_from}-{w_to} {self.units}"

#     def clean(self):
#         if not self.w_from and not self.w_to:
#             raise ValidationError(
#                 {'w_from': msg_required, 'w_to': msg_required}, code='required')

#         super().clean()

#     def validate_unique(self, exclude=None):
#         model = self._meta.model
#         if not self.w_to and model.objects.exclude(id=self.id) \
#                 .filter(w_from=self.w_from, units=self.units, w_to__isnull=True).exists():
#             raise ValidationError(
#                 {'w_from': msg_already_exists, 'units': msg_already_exists}, code='invalid')

#         if not self.w_from and model.objects.exclude(id=self.id) \
#                 .filter(w_to=self.w_to, units=self.units, w_from__isnull=True).exists():
#             raise ValidationError(
#                 {'w_to': msg_already_exists, 'units': msg_already_exists}, code='invalid')

#         super().validate_unique(exclude)

#     class Meta:
#         abstract = True
#         ordering = ('w_from', 'w_to', )
#         unique_together = (('w_from', 'w_to', 'units'),)
#         verbose_name = 'ширина взрослого растения'
#         verbose_name_plural = 'ширина взрослых растений'
