# Generated by Django 5.0.1 on 2024-03-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial_squashed_0005_rename_catalog_catalogitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='order_number',
            field=models.PositiveSmallIntegerField(verbose_name='порядковый номер'),
        ),
    ]