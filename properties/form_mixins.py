"""Shared form helpers for TTCS public-facing forms."""
from django import forms
from django.utils.translation import gettext_lazy as _


HONEYPOT_FIELD_NAME = 'website'


def honeypot_field():
    return forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'ttcs-honeypot',
            'tabindex': '-1',
            'autocomplete': 'off',
        }),
    )


def gdpr_consent_field():
    return forms.BooleanField(
        required=True,
        label=_('I consent to having my data processed for this inquiry.'),
        error_messages={'required': _('You must agree before submitting.')},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class HoneypotMixin:
    """Reject submissions when the hidden honeypot field is filled."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[HONEYPOT_FIELD_NAME] = honeypot_field()

    def clean_website(self):
        if self.cleaned_data.get(HONEYPOT_FIELD_NAME):
            raise forms.ValidationError(_('Unable to submit form.'))
        return ''


TTCS_INPUT_ATTRS = {
    'class': 'form-control',
}

TTCS_SELECT_ATTRS = {
    'class': 'form-select',
}

FIELD_ICONS = {
    'name': 'bi-person',
    'last_name': 'bi-person-badge',
    'full_name': 'bi-person',
    'email': 'bi-envelope',
    'phone': 'bi-telephone',
    'whatsapp_number': 'bi-whatsapp',
    'organization': 'bi-building',
    'job_title': 'bi-briefcase',
    'subject': 'bi-bookmark',
    'username': 'bi-person',
    'password': 'bi-lock',
    'password1': 'bi-lock',
    'password2': 'bi-lock-fill',
    'message': 'bi-chat-left-text',
    'cover_letter': 'bi-chat-left-text',
    'resume': 'bi-file-earmark-person',
    'education': 'bi-mortarboard',
    'years_experience': 'bi-bar-chart-steps',
    'department': 'bi-building',
}
