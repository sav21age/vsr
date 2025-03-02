# Generated by Django 5.0.6 on 2025-02-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_remove_video_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='code',
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='https://none.com', help_text='Под видео "... Еще" -> Экспортировать -> Прямая ссылка', max_length=255, verbose_name='ссылка'),
            preserve_default=False,
        ),
    ]
