# Generated by Django 5.0.6 on 2024-05-22 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='дата начала')),
                ('date_to', models.DateField(verbose_name='дата завершения')),
                ('name', models.CharField(help_text='Например: Ель канадская Alberta Globe C3', max_length=250, verbose_name='название')),
                ('url', models.CharField(help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/', max_length=250, verbose_name='url-адрес')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('price_old', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='старая цена, руб')),
                ('price_new', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='новая цена, руб')),
            ],
            options={
                'verbose_name': 'скидка',
                'verbose_name_plural': 'скидки',
                'ordering': ('date_from', 'date_to'),
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='дата начала')),
                ('date_to', models.DateField(verbose_name='дата завершения')),
                ('name', models.CharField(help_text='Например: 3 саженца за 1000 рублей', max_length=250, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'акция',
                'verbose_name_plural': 'акции',
                'ordering': ('date_from', 'date_to'),
            },
        ),
        migrations.CreateModel(
            name='PromotionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Например: Ель канадская Alberta Globe C3', max_length=250, verbose_name='название')),
                ('url', models.CharField(help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/', max_length=250, verbose_name='url-адрес')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='обычная цена, руб')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.promotion', verbose_name='акция')),
            ],
            options={
                'verbose_name': 'растение',
                'verbose_name_plural': 'растения',
                'ordering': ('name',),
                'unique_together': {('promotion', 'name')},
            },
        ),
    ]