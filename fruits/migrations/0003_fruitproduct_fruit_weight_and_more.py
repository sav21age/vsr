# Generated by Django 5.0.1 on 2024-03-15 14:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0002_alter_fruitproduct_beginning_fruiting'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitproduct',
            name='fruit_weight',
            field=models.CharField(blank=True, help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', max_length=12, validators=[django.core.validators.RegexValidator('^[0-9+\\-\\+\\/дот, ]+$', 'Можно вводить цифры, "/", "-" и "+"')], verbose_name='вес плодов, гр'),
        ),
        migrations.AlterField(
            model_name='fruitproduct',
            name='fruit_size',
            field=models.CharField(blank=True, help_text='Можно вводить цифры, от, до, "-". Например: 5, 5-10, от 5, до 5.', max_length=12, validators=[django.core.validators.RegexValidator('^[0-9+\\-\\+\\/дот, ]+$', 'Можно вводить цифры, "/", "-" и "+"')], verbose_name='размер плодов, см'),
        ),
    ]
