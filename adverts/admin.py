from datetime import datetime, timezone
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
# from django_ckeditor_5.widgets import CKEditor5Widget
# from pytz import timezone
from adverts.forms import AdvertAdminForm
from adverts.models import Advert
from common.widgets import formfield_overrides
# from django.forms import Textarea


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    add_form_template = "adverts/admin/add_form.html"
    change_form_template = "adverts/admin/change_form.html"
    form = AdvertAdminForm
    formfield_overrides = formfield_overrides
    list_display = ('title', 'get_body', 'created_at',)
    readonly_fields = ('created_at',)

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
    
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            delta = datetime.now(timezone.utc) - obj.created_at
            if delta.days >= 1:
                return False
        
        return True
   
    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            obj.body = mark_safe(obj.body)

        form = super().get_form(request, obj, **kwargs)

        # if 'body' in form.base_fields:
        #     form.base_fields['body'].widget = CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"},
        #     )

        return form
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        # extra_context['show_save_and_continue'] = False
        # extra_context['show_save'] = False
        # extra_context['show_delete'] = False

        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.all().count() == 1:
            # obj = self.model.objects.all()[0]
            obj = self.model.objects.get()
            return HttpResponseRedirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))
        return super().changelist_view(request=request, extra_context=extra_context)
