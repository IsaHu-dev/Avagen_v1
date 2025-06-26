from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'display_name', 'bio', 'profile_image',
            'address_line_1', 'address_line_2', 'city',
            'region', 'postal_code', 'country',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
