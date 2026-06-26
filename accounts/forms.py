from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from properties.form_mixins import HoneypotMixin


class TTCSUserCreationForm(HoneypotMixin, UserCreationForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label=_('I agree to the terms and privacy policy'),
        error_messages={'required': _('You must agree before registering.')},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta(UserCreationForm.Meta):
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username',
                'maxlength': '150',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Username')
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Password confirmation')
