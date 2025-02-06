from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class AdvertAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'body': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
        exclude = []