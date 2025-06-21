from django import forms
from .models import NewsletterSubscriber


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First Name', 'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name', 'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email',
                    'class': 'form-control'
                }
            )
        }
