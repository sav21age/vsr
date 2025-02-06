from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
# from common.helpers import codemirror_widget, textarea_widget
from common.helpers import textarea_widget


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta_description'].widget = textarea_widget
        self.fields['short_description'].widget = textarea_widget
        # self.fields['description'].widget = codemirror_widget
        self.fields['description'].required = False

        try:
            self.fields['features'].widget = textarea_widget
        except KeyError:
            pass

    class Meta:
        widgets = {
            'description': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
        exclude = []