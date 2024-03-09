# from django.urls import resolve
from django.contrib import admin
from plants.models import (
    PlantAdvantage, PlantDivision, PlantGenus, PlantPlanting,
    PlantPriceContainer, PlantPriceRootSystem)


admin.site.register(PlantDivision)


@admin.register(PlantGenus)
class PlantGenusAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', )
    list_filter = ('division',)
    search_fields = ('name',)
    search_help_text = 'Поиск по роду'

    # def get_permission(self, request):
    #     resolved = resolve(request.path_info)
    #     if resolved.url_name == 'roses_rosespecies_add':
    #         return False
    #     return True

    # def has_add_permission(self, request, obj=None):
    #     return self.get_permission(request)

    # def has_change_permission(self, request, obj=None):
    #     return self.get_permission(request)

    # def has_view_permission(self, request, obj=None):
    #     return self.get_permission(request)


class PlantSpeciesAbstractAdmin(admin.ModelAdmin):
    list_display = ('name', 'genus', )
    # list_filter = ('genus',)
    list_per_page = 40
    search_fields = ('name',)
    search_help_text = 'Поиск по виду'

admin.site.register(PlantPriceRootSystem)


admin.site.register(PlantPlanting)


@admin.register(PlantPriceContainer)
class PlantPriceContainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_number', 'description', )


admin.site.register(PlantAdvantage)