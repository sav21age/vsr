from django import forms
from django.core.validators import MinLengthValidator
from common.validators import LetterValidator, PhoneNumberValidator


class ProfileUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #     self.extra_data = kwargs.pop('extra_data', None)
        super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].initial = self.extra_data['username']
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Иван'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Иванов'

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'data-phone-pattern': '',
            'placeholder': '+X (XXX) XXX-XX-XX',
        })

    first_name = forms.CharField(
        label='Имя:', required=False, validators=[LetterValidator, MinLengthValidator(2)],)

    last_name = forms.CharField(
        label='Фамилия:', required=False, validators=[LetterValidator, MinLengthValidator(2), ])

    phone_number = forms.CharField(
        label='Телефон:',
        required=False,
        validators=[PhoneNumberValidator,],)
