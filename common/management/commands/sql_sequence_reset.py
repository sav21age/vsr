import os
from django.apps import apps
from django.core.management import call_command, BaseCommand
from django.db import connection
from io import StringIO

os.environ['DJANGO_COLORS'] = 'nocolor'


class Command(BaseCommand):
    help = 'Run sqlsequencereset for all apps'

    def handle(self, *args, **options):
        commands = StringIO()
        cursor = connection.cursor()

        for app in apps.get_app_configs():
            print(app)
            label = app.label
            call_command('sqlsequencereset', label, stdout=commands)

        cursor.execute(commands.getvalue())

