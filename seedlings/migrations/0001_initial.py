# Generated by Django 5.0.6 on 2024-10-11 09:02

import django.db.models.deletion
import easy_thumbnails.fields
import images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plants', '0002_alter_plantpricecontainer_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seedling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='название')),
                ('url', models.CharField(help_text='Url-адрес страницы с ценами. Например: /catalog/conifers/el-kanadskaya-alberta-globe/', max_length=250, verbose_name='url-адрес')),
                ('image_path', easy_thumbnails.fields.ThumbnailerImageField(max_length=200, upload_to=images.models.get_image_path, verbose_name='Путь к картинке')),
                ('image_title', models.CharField(blank=True, max_length=200, verbose_name='аттрибут title картинки')),
                ('date_shooting', models.DateField(verbose_name='дата съемки')),
                ('division', models.ForeignKey(help_text='Классификация растений: Отдел. Пример: Хвойные.', on_delete=django.db.models.deletion.CASCADE, to='plants.plantdivision', verbose_name='отдел')),
            ],
        ),
    ]