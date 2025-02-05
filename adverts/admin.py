from django.contrib import admin
from django.utils.safestring import mark_safe
from django_ckeditor_5.widgets import CKEditor5Widget
from adverts.models import Advert
from common.helpers import formfield_overrides
# from django.forms import Textarea


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    formfield_overrides = formfield_overrides
    list_display = ('title', 'get_body',)

    def get_body(self, obj):
        return mark_safe(obj.body)
    get_body.short_description = 'Текст'

    def has_add_permission(self, request):
        # check if generally has add permission
        permitted = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if permitted and Advert.objects.exists():
            permitted = False
        return permitted
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['body'].widget = Textarea(
        #     attrs={'rows': 5, 'style': 'width: 70%; font-size: 115%;'})
        
        form.base_fields['body'].widget = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"},
        )
        return form
