# Generated by Django 5.0.6 on 2024-05-16 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conifers', '0008_remove_coniferproductprice_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coniferproductprice',
            name='height_from',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20', null=True, verbose_name='высота от, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='height_to',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20', null=True, verbose_name='высота до, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='width_from',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20', null=True, verbose_name='ширина от, см'),
        ),
        migrations.AlterField(
            model_name='coniferproductprice',
            name='width_to',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, help_text='от (10) и до (пусто) =10+, от (10) и до (10) =10, от (10) и до (20) =10-20', null=True, verbose_name='ширина до, см'),
        ),
    ]