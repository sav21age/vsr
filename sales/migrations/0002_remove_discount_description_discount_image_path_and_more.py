# Generated by Django 5.0.6 on 2024-05-22 12:35

import easy_thumbnails.fields
import images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='description',
        ),
        migrations.AddField(
            model_name='discount',
            name='image_path',
            field=easy_thumbnails.fields.ThumbnailerImageField(default=1, max_length=200, upload_to=images.models.get_image_path, verbose_name='Путь к картинке'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='image_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='аттрибут title картинки'),
        ),
    ]
