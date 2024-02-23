from django.db import models
from django.contrib.contenttypes import fields
from common.models import Product
from images.models import Image
# from smart_selects.db_fields import ChainedForeignKey


class PlantDivision(models.Model):
    name = models.CharField('отдел', max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name', )
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'


class PlantGenius(models.Model):
    division = models.ForeignKey(
        PlantDivision, related_name="divisions", verbose_name='отдел', on_delete=models.DO_NOTHING)
    name = models.CharField('род', max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name', )
        verbose_name = 'род'
        verbose_name_plural = 'рода'


class PlantGroup(models.Model):
    genius = models.ForeignKey(
        PlantGenius, related_name="geniuses",  verbose_name='род', on_delete=models.DO_NOTHING)
    name = models.CharField('группа', max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name', )
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class PlantAdvantage(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'достоинства'
        verbose_name_plural = 'достоинства'


class PlantProduct(Product):

    # division = models.ForeignKey(
    #     PlantDivision, verbose_name='отдел', on_delete=models.DO_NOTHING)

    # genius = models.ForeignKey(
    #     PlantGenius, verbose_name='род', on_delete=models.DO_NOTHING)

    group = models.ForeignKey(
        PlantGroup, verbose_name='группа', on_delete=models.DO_NOTHING)

    # genius = ChainedForeignKey(PlantGenius, verbose_name='род',
    #                            chained_field='division', chained_model_field='division',
    #                            show_all=False, auto_choose=False, sort=True)

    # group = ChainedForeignKey(PlantGroup, verbose_name='группа',
    #                           chained_field='genius', chained_model_field='genius',
    #                           show_all=False, auto_choose=False, sort=True)

    # name = models.CharField('название', max_length=100)
    # images = fields.GenericRelation(Image)

    # def __str__(self):
    #     return str(self.name)
    size = models.CharField('размер', max_length=200)

    # advantages = models.CharField('достоинства', max_length=200)
    advantages = models.ManyToManyField(
        PlantAdvantage, verbose_name='достоинства', related_name='+',
        blank=True,)

    features = models.CharField('особенности', max_length=250)

    class Meta:
        ordering = ('group', )
        verbose_name = 'растение'
        verbose_name_plural = 'растения'


class PlantPriceHeight(models.Model):
    h_from = models.IntegerField('высота, от')
    h_to = models.IntegerField('высота, до')

    def __str__(self):
        return f"{self.h_from}-{self.h_to}"

    class Meta:
        ordering = ('h_from', 'h_to', )
        verbose_name = 'высота'
        verbose_name_plural = 'высота'


class PlantPriceTrunkDiameter(models.Model):
    tt_from = models.IntegerField('диаметр ствола, от')
    tt_to = models.IntegerField('диаметр ствола, до')

    def __str__(self):
        return f"{self.tt_from}-{self.tt_to}"

    class Meta:
        ordering = ('tt_from', 'tt_to', )
        verbose_name = 'диаметр ствола'
        verbose_name_plural = 'диаметр стволов'


class PlantPriceWidth(models.Model):
    w_from = models.IntegerField('ширина, от')
    w_to = models.IntegerField('ширина, до')

    def __str__(self):
        return f"{self.w_from}-{self.w_to}"

    class Meta:
        ordering = ('w_from', 'w_to', )
        verbose_name = 'ширина'
        verbose_name_plural = 'ширина'


class PlantPriceRootSystem(models.Model):
    abbr_ru = models.CharField('аббревиатура на русском языке', max_length=10)
    abbr_en = models.CharField('аббревиатура на английском', max_length=10)
    description = models.TextField('описание',)

    def __str__(self):
        return f"{self.abbr_ru}"

    class Meta:
        verbose_name = 'корневая система'
        verbose_name_plural = 'корневые системы'


class PlantPriceContainer(models.Model):
    abbr_en = models.CharField('аббревиатура на английском', max_length=5)
    description = models.TextField('описание', max_length=100)

    def __str__(self):
        return f"{self.abbr_en}"

    class Meta:
        ordering = ('abbr_en', )
        verbose_name = 'контейнер'
        verbose_name_plural = 'контейнеры'


class PlantPrice(models.Model):
    product = models.ForeignKey(
        PlantProduct, verbose_name='растение', on_delete=models.DO_NOTHING)

    container = models.ForeignKey(
        PlantPriceContainer, verbose_name='контейнер', blank=True, null=True, on_delete=models.DO_NOTHING)

    tt = models.ForeignKey(
        PlantPriceTrunkDiameter, verbose_name='диаметр ствола', blank=True, null=True, on_delete=models.DO_NOTHING)

    rs = models.ForeignKey(
        PlantPriceRootSystem, verbose_name='корневая система', blank=True, null=True, on_delete=models.DO_NOTHING)

    height = models.ForeignKey(
        PlantPriceHeight, verbose_name='высота', blank=True, null=True, on_delete=models.DO_NOTHING)

    width = models.ForeignKey(
        PlantPriceWidth, verbose_name='ширина', blank=True, null=True, on_delete=models.CASCADE)

    price = models.DecimalField('цена', max_digits=9, decimal_places=2)

    order_number = models.PositiveSmallIntegerField(
        'порядковый номер', default=0)

    def __str__(self):
        s = ''

        if self.container:
            s = f"{self.container}"

        if self.tt:
            s = f"{self.tt}" if len(s) == 0 else f"{s} {self.tt}"

        if self.height:
            s = f"{self.height}" if len(s) == 0 else f"{s} {self.height}"

        if self.width:
            s = f"{self.width}" if len(s) == 0 else f"{s} {self.width}"

        if self.rs:
            s = f"{self.rs}" if len(s) == 0 else f"{s} {self.rs}"

        return f"{self.price}" if len(s) == 0 else f"{s} {self.price}"

    class Meta:
        ordering = ('order_number',)
        verbose_name = 'цена'
        verbose_name_plural = 'цены'
