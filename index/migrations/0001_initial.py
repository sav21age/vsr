# Generated by Django 5.0.1 on 2024-01-29 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_title', models.CharField(max_length=80, verbose_name='заголовок')),
                ('meta_description', models.CharField(max_length=160, verbose_name='мета описание')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='название')),
                ('slug', models.SlugField(max_length=80, unique=True, verbose_name='слаг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('is_visible', models.BooleanField(db_index=True, default=1, verbose_name='показывать')),
                ('about_us', models.TextField(verbose_name='о нас')),
            ],
            options={
                'verbose_name': 'главная страница',
                'verbose_name_plural': 'главная страница',
            },
        ),
    ]
