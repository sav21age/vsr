from django.contrib import admin
from common.admin import PageAbstractAdmin
from index.forms import IndexAdminForm
from index.models import Index
from solo.admin import SingletonModelAdmin
from common.helpers import formfield_overrides


@admin.register(Index)
class IndexAdmin(PageAbstractAdmin, SingletonModelAdmin):
    form = IndexAdminForm
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets + (
            ('', {
                    'fields': (
                        'about_us',
                    )
                }),
        )