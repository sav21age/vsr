# Generated by Django 5.0.1 on 2024-02-28 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perennials', '0001_initial'),
        ('plants', '0002_alter_plantgenus_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='perspecies',
            unique_together={('name', 'genus')},
        ),
    ]