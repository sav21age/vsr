# Generated by Django 5.0.1 on 2024-05-07 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conifers', '0007_alter_coniferproductprice_extra_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coniferproductprice',
            name='height',
        ),
        migrations.RemoveField(
            model_name='coniferproductprice',
            name='width',
        ),
    ]
