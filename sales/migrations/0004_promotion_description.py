# Generated by Django 5.0.6 on 2024-05-22 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_remove_promotion_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='description',
            field=models.TextField(blank=True, verbose_name='описание'),
        ),
    ]