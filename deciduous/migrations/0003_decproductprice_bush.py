# Generated by Django 5.0.1 on 2024-03-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deciduous', '0002_alter_decproduct_inflorescence'),
    ]

    operations = [
        migrations.AddField(
            model_name='decproductprice',
            name='bush',
            field=models.BooleanField(default=False, help_text='Кустовая, многоствольная форма.', verbose_name='куст'),
        ),
    ]
