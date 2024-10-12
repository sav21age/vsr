from django import forms
from images.widgets import ImageAdminWidget
from seedlings.models import Seedling


class SeedlingAdminForm(forms.ModelForm):
    class Meta:
        model = Seedling
        widgets = {
            'image_path': ImageAdminWidget(),
        }
        exclude = []

