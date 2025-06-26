from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'profiles/custom_clearable_file_input.html'


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
            'profile_image': CustomClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
