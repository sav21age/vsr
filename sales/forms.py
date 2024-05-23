from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from sales.models import Discount, Promotion
from images.widgets import ImageAdminWidget


class DiscountAdminForm(forms.ModelForm):
    class Meta:
        model = Discount
        widgets = {
            'image_path': ImageAdminWidget(),
        }
        exclude = []


class PromotionAdminForm(forms.ModelForm):
    class Meta:
        model = Promotion
        widgets = {
            'description': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
        exclude = []
