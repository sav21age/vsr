from django.contrib import admin
from solo.admin import SingletonModelAdmin
from pricelist.models import PriceList


@admin.register(PriceList)
class PriceListAdmin(SingletonModelAdmin):
    pass
