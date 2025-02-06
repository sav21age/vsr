# from django.db import models
# from common.validators import SizeValidator
# from django.core.validators import RegexValidator
# from plants.models import PlantPlanting


# class PlantPlantingFieldAbstract(models.Model):
#     # CHOICES_PLANTING = (
#     #     ('солнце', 'солнце'),
#     #     ('тень', 'тень'),
#     #     ('полутень', 'полутень'),
#     # )
#     # planting = models.CharField('место посадки', max_length=15, choices=CHOICES_PLANTING,
#     #                             blank=True, null=True, default=None, )

#     planting = models.ManyToManyField(
#         PlantPlanting, verbose_name='место посадки', related_name='+',
#         blank=True,)

#     class Meta:
#         abstract = True


# class PlantWinterZoneFieldAbstract(models.Model):
#     CHOICES_WINTER_ZONE = (
#         ('6 (-23)', '6 (-23)'),
#         ('5 (-29)', '5 (-29)'),
#         ('4 (-34)', '4 (-34)'),
#         ('3 (-40)', '3 (-40)'),
#     )
#     winter_zone = models.CharField('зона зимостойкости, в градусах', max_length=15, choices=CHOICES_WINTER_ZONE,
#                                    blank=True, null=True, default=None, )

#     class Meta:
#         abstract = True


# class PlantFloweringPeriodFieldAbstract(models.Model):
#     flowering_period = models.CharField(
#         'период цветения', max_length=7, blank=True,
#         validators=(RegexValidator(
#             r'(IX|IV|V?I{0,3}|\-)', 'Можно вводить только римские цифры и "-"'),),
#         help_text='Можно вводить только римские цифры и "-". Например: IV, IV-VI.', )

#     class Meta:
#         abstract = True


# class PlantFlowerSizeFieldAbstract(models.Model):
#     flower_size = models.CharField(
#         'размер цветка, см', max_length=7, blank=True,
#         validators=(SizeValidator,),
#         help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )
    
#     class Meta:
#         abstract = True


# class PlantInflorescenceSizeFieldAbstract(models.Model):
#     inflorescence_size = models.CharField(
#         'размер соцветия, см', max_length=7, blank=True,
#         validators=(SizeValidator,),
#         help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', )
    
#     class Meta:
#         abstract = True


# class PlantShtambFieldAbstract(models.Model):
#     shtamb = models.CharField(
#         'штамб', max_length=7, blank=True, validators=(SizeValidator,),
#         help_text='Ветвление на стволе начинается c указанной высоты, см.')

#     class Meta:
#         abstract = True
