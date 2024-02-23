from django import forms
from django_recaptcha.fields import ReCaptchaField
from orders.models import Order


class CreateOrderAuthUserForm(forms.ModelForm):
    # email_on_change_status = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # attrs={'class':'form-control',}
        # for field in self.fields.values():
        #     field.widget.attrs = attrs

        # self.fields['customer_phone_number'].required = False
        # self.fields['customer_name'].required = True

        if self.user.profile.phone_number:
            self.fields.pop('customer_phone_number')
        else:
            self.fields['customer_phone_number'].widget.attrs.update({
                'data-phone-pattern': '',
            })

        if self.user.first_name:
            self.fields.pop('customer_first_name')

        if self.user.last_name:
            self.fields.pop('customer_last_name')

        if self.user.email:
            self.fields.pop('customer_email')

        self.fields['customer_comment'].widget.attrs.update({
            'rows': 3,
        })

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        exclude = ['user', 'number', 'status_change_email', 'confirm_code', 'confirmed_by_email',
                   'ip', 'user_agent', 'status', ]


class CreateOrderAnonymUserForm(forms.ModelForm):
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['customer_comment'].widget.attrs.update({
            'rows': 3,
        })

        self.fields['customer_phone_number'].widget.attrs.update({
            'data-phone-pattern': '',
        })

        for field in self.fields:
            if field != 'captcha':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = Order
        exclude = ['user', 'number', 'status_change_email', 'confirm_code', 'confirmed_by_email',
                   'ip', 'user_agent', 'status', ]


class ConfirmOrderAnonymUserForm(forms.Form):
    confirm_code = forms.CharField(
        label='Введите код',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm_code'].widget.attrs['class'] = 'form-control'

