from django.contrib import admin
from solo.admin import SingletonModelAdmin

from common.helpers import formfield_overrides, codemirror_widget
from contacts.models import Contacts, WorkSchedule


@admin.register(WorkSchedule)
class WorkScheduleAdmin(SingletonModelAdmin):
    pass


@admin.register(Contacts)
class ContactsAdmin(SingletonModelAdmin):
    save_on_top = False
    formfield_overrides = formfield_overrides

    fieldsets = (
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
    
    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request, obj)
    #     return fieldsets + (
    #         ('Реквизиты', {
    #                 'fields': (
    #                     'company_name',
    #                     'inn',
    #                     'ogrn',
    #                     'kpp',
    #                 )
    #             }),
    #         ('Контактная информация', {
    #                 'fields': (
    #                     'address',
    #                     'phone_retail',
    #                     'phone_wholesale',
    #                     'email',
    #                     'map',
    #                 )
    #             }),
    #     )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['map'].widget.attrs['rows'] = 7
        form.base_fields['map'].widget = codemirror_widget
        return form
