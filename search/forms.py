from django import forms
from django.core.validators import MinLengthValidator


class SearchForm(forms.Form):
    q = forms.CharField(max_length=50, required=False,
        validators=[MinLengthValidator(2)],
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].widget.attrs['class'] = 'form-control'
        # self.fields['q'].widget.attrs['data-selectable-options'] = {'highlightMatch': False, 'minLength': 2}
        self.fields['q'].widget.attrs['data-selectable-options'] = {'minLength': 2}
        self.fields['q'].widget.attrs['placeholder'] = 'поиск...'

