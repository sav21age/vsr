# Generated by Django 5.0.1 on 2024-03-21 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0006_fruitproduct_self_fertility'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitProductPriceRootstock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rootstock', models.PositiveSmallIntegerField(choices=[(1, 'полукарликовый'), (2, 'семенной')], default=1, unique=True, verbose_name='подвой')),
            ],
            options={
                'verbose_name': 'подвой растения',
                'verbose_name_plural': 'подвой растений',
                'ordering': ('rootstock',),
            },
        ),
        migrations.RemoveField(
            model_name='fruitproduct',
            name='rootstock',
        ),
        migrations.AddField(
            model_name='fruitproductprice',
            name='rootstock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruits.fruitproductpricerootstock', verbose_name='подвой'),
        ),
    ]
