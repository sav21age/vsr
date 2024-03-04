from django import forms
from catalog.models import CatalogItem
from images.widgets import ImageAdminWidget


class CatalogItemAdminForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        widgets = {
            'image_path': ImageAdminWidget(),
        }
        exclude = []
