from django_recaptcha.fields import ReCaptchaField
from allauth.account.forms import (
    SignupForm, LoginForm, ChangePasswordForm, SetPasswordForm,
    ResetPasswordForm, ResetPasswordKeyForm)


class RecaptchaSignupForm(SignupForm):
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'captcha':
                self.fields[field].widget.attrs.update({
                    # 'style': 'transform:scale(0.8); transform-origin:0;',
                    # 'data-size': 'compact',
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': '',
                    'autocomplete': 'off'
                })

    field_order = ['email', 'password1', 'password2', 'captcha',]


class RecaptchaResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'captcha':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': '',
                    # 'autocomplete': 'off'
                })


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'remember':
                self.fields[field].widget.attrs.update({
                    'style': 'accent-color: #66651F; width: 15px; height: 15px;',
                    'checked': True,
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': '',
                    # 'autocomplete': 'off'
                })


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off'
            })


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off'
            })


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off'
            })