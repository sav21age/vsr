# Generated by Django 5.0.1 on 2024-03-21 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otherproductprice',
            old_name='property',
            new_name='name',
        ),
    ]