from django import forms
from common.widgets import codemirror_widget, textarea_widget


class IndexAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta_description'].widget = textarea_widget
        
        self.fields['con_short_description'].widget = textarea_widget
        self.fields['dec_short_description'].widget = textarea_widget
        self.fields['fru_short_description'].widget = textarea_widget
        self.fields['per_short_description'].widget = textarea_widget

        self.fields['description'].widget = codemirror_widget
        
        self.fields['con_description'].widget = codemirror_widget
        self.fields['dec_description'].widget = codemirror_widget
        self.fields['fru_description'].widget = codemirror_widget
        self.fields['per_description'].widget = codemirror_widget

    class Meta:
        exclude = []