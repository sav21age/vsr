# Generated by Django 5.0.6 on 2024-05-17 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0011_auto_20240517_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fruitproductprice',
            name='height',
        ),
        migrations.RemoveField(
            model_name='fruitproductprice',
            name='width',
        ),
    ]
