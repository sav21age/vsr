from django.contrib import admin
from common.admin import PageAbstractAdmin
from contacts.models import Contacts, WorkSchedule
from solo.admin import SingletonModelAdmin
from common.helpers import codemirror_widget


@admin.register(WorkSchedule)
class WorkScheduleAdmin(SingletonModelAdmin):
    pass


@admin.register(Contacts)
class ContactsAdmin(PageAbstractAdmin, SingletonModelAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets + (
            ('Реквизиты', {
                    'fields': (
                        'company_name',
                        'inn',
                        'ogrn',
                        'kpp',
                    )
                }),
            ('Контактная информация', {
                    'fields': (
                        'address',
                        'phone_retail',
                        'phone_wholesale',
                        'email',
                        'map',
                    )
                }),
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['map'].widget.attrs['rows'] = 7
        form.base_fields['map'].widget = codemirror_widget
        return form
