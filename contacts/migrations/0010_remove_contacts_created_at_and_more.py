# Generated by Django 5.0.6 on 2025-02-26 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_alter_workschedule_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacts',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='head_title',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='is_visible',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='updated_at',
        ),
    ]
