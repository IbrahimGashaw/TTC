from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Contact, Property, PropertyBooking, ViewingAppointment, PropertyNeedRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'last_name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Message'}),
        }


class PropertyInquiryForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PropertySearchForm(forms.Form):
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by location'}))
    property_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Property Type')] + Property.PROPERTY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bedrooms', 'min': 0}))
    bathrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bathrooms', 'min': 0}))
    min_price = forms.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Min Price (ETB)'),
            'min': 0,
            'step': 1000
        })
    )
    max_price = forms.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Max Price (ETB)'),
            'min': 0,
            'step': 1000
        })
    )
    sale_type = forms.ChoiceField(
        required=False,
        choices=[('', _('Sale Type'))] + Property.SALE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Status')] + Property.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError(_('Minimum price cannot be greater than maximum price.'))
        
        return cleaned_data


class PropertyBookingForm(forms.ModelForm):
    class Meta:
        model = PropertyBooking
        fields = ['full_name', 'email', 'phone', 'id_number', 'start_date', 'end_date', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'required': True}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'full_name': _('Full Name'),
            'email': _('Email'),
            'phone': _('Phone'),
            'id_number': _('ID Number'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'notes': _('Additional Notes'),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(_('End date must be after start date.'))
            
            if start_date < timezone.now():
                raise forms.ValidationError(_('Start date cannot be in the past.'))
        
        return cleaned_data


class ViewingAppointmentForm(forms.ModelForm):
    """Quick form for booking property viewings"""
    class Meta:
        model = ViewingAppointment
        fields = ['full_name', 'email', 'phone', 'whatsapp_number', 'preferred_date', 'preferred_time', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your full name'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your email address'),
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your phone number'),
                'required': True
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('WhatsApp number (optional)')
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'min': timezone.now().date().isoformat()
            }),
            'preferred_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Any additional information or special requests')
            }),
        }
        labels = {
            'full_name': _('Full Name'),
            'email': _('Email'),
            'phone': _('Phone Number'),
            'whatsapp_number': _('WhatsApp Number (Optional)'),
            'preferred_date': _('Preferred Date'),
            'preferred_time': _('Preferred Time'),
            'notes': _('Additional Notes'),
        }
    
    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError(_('Preferred date cannot be in the past.'))
        return date


class PropertyNeedRequestForm(forms.ModelForm):
    class Meta:
        model = PropertyNeedRequest
        fields = [
            'full_name', 'email', 'phone', 'whatsapp_number',
            'preferred_location', 'property_type', 'sale_type',
            'bedrooms_min', 'bedrooms_max', 'bathrooms_min', 'bathrooms_max',
            'budget_min', 'budget_max', 'size_min', 'size_max',
            'move_in_timeline', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'sale_type': forms.Select(attrs={'class': 'form-select'}),
            'bedrooms_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bedrooms_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bathrooms_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bathrooms_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1000}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1000}),
            'size_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'size_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'move_in_timeline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g., 1-3 months')}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        min_budget = cleaned_data.get('budget_min')
        max_budget = cleaned_data.get('budget_max')
        if min_budget and max_budget and min_budget > max_budget:
            raise forms.ValidationError(_('Minimum budget cannot exceed maximum budget.'))
        bed_min = cleaned_data.get('bedrooms_min')
        bed_max = cleaned_data.get('bedrooms_max')
        if bed_min and bed_max and bed_min > bed_max:
            raise forms.ValidationError(_('Minimum bedrooms cannot exceed maximum bedrooms.'))
        bath_min = cleaned_data.get('bathrooms_min')
        bath_max = cleaned_data.get('bathrooms_max')
        if bath_min and bath_max and bath_min > bath_max:
            raise forms.ValidationError(_('Minimum bathrooms cannot exceed maximum bathrooms.'))
        size_min = cleaned_data.get('size_min')
        size_max = cleaned_data.get('size_max')
        if size_min and size_max and size_min > size_max:
            raise forms.ValidationError(_('Minimum size cannot exceed maximum size.'))
        return cleaned_data

