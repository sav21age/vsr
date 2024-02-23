from django.contrib import admin
from pricelist.models import PriceList
from solo.admin import SingletonModelAdmin


@admin.register(PriceList)
class PriceListAdmin(SingletonModelAdmin):
    pass
