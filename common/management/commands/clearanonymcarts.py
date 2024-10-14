import time
import datetime
import pytz
from django.core.management.base import BaseCommand
from django.conf import settings
from carts.models import Cart


class Command(BaseCommand):
    help = 'Clear expired anonymous carts'

    def handle(self, *args, **kwargs):
        date_diff = time.time() - settings.SESSION_COOKIE_AGE
        tz = pytz.timezone(settings.TIME_ZONE)
        date_expire = datetime.datetime.fromtimestamp(date_diff, tz)

        Cart.objects.filter(user__isnull=True).filter(
            updated_at__lt=date_expire).delete()
        
        # qs = Cart.objects.filter(user__isnull=True).filter(updated_at__lt=date)
        # print(qs)