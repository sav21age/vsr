from django.contrib import admin
from common.admin import PageAbstractAdmin
from index.forms import IndexAdminForm
from index.models import Index
from solo.admin import SingletonModelAdmin
# from common.helpers import formfield_overrides


@admin.register(Index)
class IndexAdmin(PageAbstractAdmin, SingletonModelAdmin):
    form = IndexAdminForm
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets + (
            ('О нас', {
                    'fields': (
                        'description',
                    )
            }),
            ('Хвойные растения', {
                    'fields': (
                        'con_visible', 'con_name', 'con_short_description', 'con_description',
                    )
            }),
            ('Лиственные растения', {
                    'fields': (
                        'dec_visible', 'dec_name', 'dec_short_description', 'dec_description',
                    )
            }),
            ('Многолетние растения', {
                    'fields': (
                        'per_visible', 'per_name', 'per_short_description', 'per_description',
                    )
            }),
            ('Фруктовые растения', {
                'fields': (
                    'fru_visible', 'fru_name', 'fru_short_description', 'fru_description',
                )
            }),
        )
