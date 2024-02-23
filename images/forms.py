from django import forms
from images.models import Image
from images.widgets import ImageAdminWidget

class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        widgets = {
            'path': ImageAdminWidget(),
        }
        exclude = []
