"""Custom checkout form implementation for Avagen.
"""
from django import forms
from django.core.validators import RegexValidator
from .models import Order
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class OrderForm(forms.ModelForm):
    country = forms.ChoiceField(  
    choices=list(CountryField().choices),
    widget=CountrySelectWidget(layout='{widget}')  # Disable stripe's flag icon
    )
    # Custom field validators
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'."
    )
    
    # Override default fields with custom widgets
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        required=True,
        error_messages={
            'required': 'Please enter a valid phone number',
            'invalid': 'Please enter a valid phone number format'
        }
    )
    
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Please enter a valid email address',
            'invalid': 'Please enter a valid email format'
        }
    )

    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Features:
        - Dynamic placeholder system
        """
        super().__init__(*args, **kwargs)
        
        # Placeholder system with icons
        placeholders = {
            'full_name': '👤 Full Name',
            'email': '📧 Email Address',
            'phone_number': '📱 Phone Number',
            'postcode': '📮 Postal Code',
            'town_or_city': '🏙️ Town or City',
            'street_address1': '📍 Street Address 1',
            'street_address2': '📍 Street Address 2',
            'county': '🏘️ County, State or Locality',
        }

        style_classes = {
            'full_name': 'form-control name-input',
            'email': 'form-control email-input',
            'phone_number': 'form-control phone-input',
            'postcode': 'form-control postcode-input',
            'town_or_city': 'form-control city-input',
            'street_address1': 'form-control address-input',
            'street_address2': 'form-control address-input',
            'county': 'form-control county-input',
            'country': 'form-control country-select'
        }

        self.fields['full_name'].widget.attrs.update({
            'autofocus': True,
            'class': f'{style_classes["full_name"]} focus-ring',
            'data-validate': 'required'
        })
        
        for field in self.fields:
            # Skip country field special handling
            if field != 'country':
                # Placeholder with required indicator
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                
                # Apply field-specific styling and attributes
                attrs = {
                    'placeholder': placeholder,
                    'class': f'{style_classes[field]} stripe-style-input',
                    'data-validate': 'required' if self.fields[field].required else '',
                    'aria-label': placeholders[field].replace(' *', '')
                }
                self.fields[field].widget.attrs.update(attrs)
            else:
                # Special handling for country field
                self.fields[field].widget.attrs.update({
                    'class': f'{style_classes[field]} stripe-style-input',
                    'data-validate': 'required'
                })
            
            # Remove default labels as we're using placeholders
            self.fields[field].label = False

        self.fields['country'].widget.attrs['class'] = 'stripe-style-input'
        self.fields['country'].label = 'Country'
        self.fields['country'].required = True
