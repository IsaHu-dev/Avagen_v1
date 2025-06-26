# Import Django's forms library and utilities to get the active User model
from django import forms
from django.contrib.auth import get_user_model

# Import the custom user profile model
from .models import UserProfile

# Get the currently active User model (custom or default)
User = get_user_model()

# Custom file input widget with a custom template
class CustomClearableFileInput(forms.ClearableFileInput):
    # Use a custom template for rendering the file input (e.g., with preview or delete option)
    template_name = 'profiles/custom_clearable_file_input.html'


# Form for editing a user's profile (not the core auth user)
class UserProfileForm(forms.ModelForm):
    class Meta:
        # Link the form to the UserProfile model
        model = UserProfile
        # Specify which fields from the model to include in the form
        fields = [
            'display_name', 'bio', 'profile_image',
            'address_line_1', 'address_line_2', 'city',
            'region', 'postal_code', 'country',
        ]
        # Customize the widget rendering for specific fields
        widgets = {
            # Use a smaller textarea for the bio field
            'bio': forms.Textarea(attrs={'rows': 3}),
            # Use the custom file input widget for profile_image with extra HTML attributes
            'profile_image': CustomClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }


# Form for updating core User model data (first name, last name, email)
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        # Link the form to the User model
        model = User
        # Include only editable fields from the User model
        fields = ['first_name', 'last_name', 'email']
