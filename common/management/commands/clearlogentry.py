from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry


class Command(BaseCommand):
    help = 'Clear admin history'

    def handle(self, *args, **kwargs):
        delta = datetime.now(timezone.utc) - timedelta(days=30)
        LogEntry.objects.filter(action_time__lt=delta).delete()
        self.stdout.write('Admin history cleared.')
