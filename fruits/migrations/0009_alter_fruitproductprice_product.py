# Generated by Django 5.0.1 on 2024-03-31 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0008_alter_fruitproductpricerootstock_rootstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruitproductprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='fruits.fruitproduct', verbose_name='растение'),
        ),
    ]