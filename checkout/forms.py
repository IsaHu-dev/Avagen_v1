"""
Digital Purchase Forms for Avagen Marketplace
=============================================

This module defines forms for digital product purchases including:
- Customer information collection
- Billing address validation
- License selection

Author: Isa Hu
Date: 2024
License: MIT License
Original Work: This is original code written specifically for the
Avagen project. No external code was copied or plagiarized.

Dependencies:
- Django 4.2+
- django-countries
"""

from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import DigitalPurchase


class UserInfoForm(forms.ModelForm):
    """
    Form for collecting user information and billing details
    """
    
    # Custom validators
    phone_validator = RegexValidator(
        regex=r'^[\+]?[1-9][\d]{0,15}$',
        message="Please enter a valid phone number (e.g., +1234567890)"
    )
    
    email_validator = EmailValidator(
        message="Please enter a valid email address"
    )
    
    # Override fields with custom validation
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control customer-name',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        }),
        error_messages={
            'required': 'Please provide your full name',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    
    customer_email = forms.EmailField(
        validators=[email_validator],
        widget=forms.EmailInput(attrs={
            'class': 'form-control customer-email',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email'
        }),
        error_messages={
            'required': 'Please provide your email address',
            'invalid': 'Please enter a valid email format'
        }
    )
    
    contact_phone = forms.CharField(
        max_length=25,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control contact-phone',
            'placeholder': 'Phone number (optional)',
            'autocomplete': 'tel'
        }),
        error_messages={
            'invalid': 'Please enter a valid phone number'
        }
    )
    
    # Billing address fields
    billing_country = forms.ChoiceField(
        choices=list(CountryField().choices),
        widget=CountrySelectWidget(attrs={
            'class': 'form-control billing-country',
            'data-placeholder': 'Select your country'
        }),
        error_messages={
            'required': 'Please select your country',
            'invalid_choice': 'Please select a valid country'
        }
    )
    
    billing_city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control billing-city',
            'placeholder': 'City or town',
            'autocomplete': 'address-level2'
        }),
        error_messages={
            'required': 'Please provide your city',
            'max_length': 'City name cannot exceed 50 characters'
        }
    )
    
    billing_postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control billing-postal',
            'placeholder': 'Postal/ZIP code (optional)',
            'autocomplete': 'postal-code'
        })
    )
    
    billing_address_line1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control billing-address-1',
            'placeholder': 'Street address line 1',
            'autocomplete': 'address-line1'
        }),
        error_messages={
            'required': 'Please provide your street address',
            'max_length': 'Address cannot exceed 100 characters'
        }
    )
    
    billing_address_line2 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control billing-address-2',
            'placeholder': 'Street address line 2 (optional)',
            'autocomplete': 'address-line2'
        })
    )
    
    billing_state = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control billing-state',
            'placeholder': 'State/Province/Region (optional)',
            'autocomplete': 'address-level1'
        })
    )
    
    # Terms and conditions
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input terms-checkbox',
            'id': 'accept-terms'
        }),
        error_messages={
            'required': 'You must accept the terms and conditions'
        }
    )
    
    class Meta:
        model = DigitalPurchase
        fields = [
            'customer_name', 'customer_email', 'contact_phone',
            'billing_country', 'billing_city', 'billing_postal_code',
            'billing_address_line1', 'billing_address_line2', 'billing_state',
            'accept_terms'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add field-specific styling and validation
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                # Add data attributes for client-side validation
                field.widget.attrs.update({
                    'data-field': field_name,
                    'aria-describedby': f'{field_name}-help'
                })
    
    def clean_customer_name(self):
        """Custom validation for customer name"""
        name = self.cleaned_data.get('customer_name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError(
                'Name must be at least 2 characters long'
            )
        return name.strip()
    
    def clean_customer_email(self):
        """Custom validation for email"""
        email = self.cleaned_data.get('customer_email')
        if email:
            # Check for common disposable email domains
            disposable_domains = ['tempmail.com', 'throwaway.com']
            domain = email.split('@')[1].lower()
            if domain in disposable_domains:
                raise forms.ValidationError(
                    'Please use a valid email address'
                )
        return email.lower()
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        # Validate that required fields are present
        required_fields = [
            'customer_name', 'customer_email', 'billing_country',
            'billing_city', 'billing_address_line1'
        ]
        
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required')
        
        return cleaned_data


class LicenseSelectionForm(forms.Form):
    """
    Form for selecting license types for digital products
    """
    
    LICENSE_CHOICES = [
        ('personal', 'Personal License - $9.99'),
        ('commercial', 'Commercial License - $29.99'),
        ('extended', 'Extended License - $49.99'),
    ]
    
    license_type = forms.ChoiceField(
        choices=LICENSE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input license-radio'
        }),
        initial='personal',
        error_messages={
            'required': 'Please select a license type',
            'invalid_choice': 'Please select a valid license type'
        }
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'min': '1',
            'max': '10'
        }),
        error_messages={
            'required': 'Please specify quantity',
            'min_value': 'Quantity must be at least 1',
            'max_value': 'Maximum quantity is 10'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text for license types
        self.fields['license_type'].help_text = (
            'Choose the appropriate license for your intended use'
        )
        self.fields['quantity'].help_text = (
            'Number of licenses to purchase (1-10)'
        )


class UserCheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        }),
        label='Full name',
        required=True
    )
    user_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        }),
        label='Full email',
        required=True
    )
    contact_phone = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number (optional)',
            'autocomplete': 'tel'
        }),
        label='Contact phone',
        required=False
    )
