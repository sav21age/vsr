# Generated by Django 5.0.1 on 2024-03-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0005_alter_fruitproduct_fruit_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitproduct',
            name='self_fertility',
            field=models.CharField(blank=True, max_length=20, verbose_name='самоплодность'),
        ),
    ]