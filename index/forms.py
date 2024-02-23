from django import forms
from common.helpers import codemirror_widget, textarea_widget


class IndexAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta_description'].widget = textarea_widget
        self.fields['about_us'].widget = codemirror_widget

    class Meta:
        exclude = []