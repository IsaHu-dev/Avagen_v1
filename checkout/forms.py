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
        widget=CountrySelectWidget(layout='{widget}')
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
        Initialize form with placeholders and styling
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

        # Apply styling and placeholders to all fields
        for field in self.fields:
            if field != 'country':
                # Placeholder with required indicator
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                
                # Apply field-specific styling and attributes
                data_validate = 'required' if self.fields[field].required else ''
                aria_label = placeholders[field].replace(' *', '')
                attrs = {
                    'placeholder': placeholder,
                    'class': 'form-control stripe-style-input',
                    'data-validate': data_validate,
                    'aria-label': aria_label
                }
                self.fields[field].widget.attrs.update(attrs)
            else:
                # Special handling for country field
                self.fields[field].widget.attrs.update({
                    'class': 'form-control stripe-style-input',
                    'data-validate': 'required'
                })
            
            # Remove default labels as we're using placeholders
            self.fields[field].label = False

        # Set autofocus on first field
        self.fields['full_name'].widget.attrs['autofocus'] = True
