# Generated by Django 5.0.1 on 2024-05-02 16:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conifers', '0006_auto_20240502_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coniferproductprice',
            name='extra',
            field=models.BooleanField(db_index=True, default=False, help_text='Ухоженные растения.', verbose_name='экстра'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='height_from',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='высота от, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='height_to',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='высота до, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='shtamb',
            field=models.CharField(blank=True, db_index=True, help_text='Ветвление на стволе начинается c указанной высоты, см.', max_length=7, validators=[django.core.validators.RegexValidator('^[0-9+\\-\\+\\/дот, ]+$', 'Можно вводить цифры, "/", "-" и "+"')], verbose_name='штамб, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='width_from',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='ширина от, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='width_to',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='ширина до, см'),
        ),
    ]