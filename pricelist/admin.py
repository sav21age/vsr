from django.contrib import admin
from solo.admin import SingletonModelAdmin

from pricelist.models import PriceList


@admin.register(PriceList)
class PriceListAdmin(SingletonModelAdmin):
    save_on_top = False
    fields = ('file_path', )

    # fieldsets = (
    #     ('Промо', {
    #         'fields': ('head_title', 'meta_description',)
    #     }),
    #     ('', {
    #         'fields': ('name', 'slug',)
    #     }),
    #     ('Файл', {
    #         'fields': ('file_path',)
    #     }),

    # )

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request, obj)
    #     return fieldsets + (
    #         ('Файл', {
    #             'fields': ('file_path',)
    #         }),
    #     )
