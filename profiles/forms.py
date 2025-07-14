# Import Django's forms library and utilities to get the active User model

from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

# Import the custom user profile model

from .models import UserProfile

# Get the currently active User model (custom or default)

User = get_user_model()

# Allowed image extensions

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp"]


# Form for editing a user's profile (not the core auth user)


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
        ],
    )

    class Meta:
        # Link the form to the UserProfile model

        model = UserProfile
        # Specify which fields from the model to include in the form

        fields = [
            "display_name",
            "bio",
            "profile_image",
            "address_line_1",
            "address_line_2",
            "city",
            "region",
            "postal_code",
            "country",
        ]
        # Customize the widget rendering for specific fields

        widgets = {
            # Use a smaller textarea for the bio field
            "bio": forms.Textarea(attrs={"rows": 3}),
            # Use standard file input for profile_image
            "profile_image": forms.FileInput(
                attrs={"class": "form-control-file", "accept": "image/*"}
            ),
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image", False)
        # If the field is empty or cleared, allow it without error

        if image in [None, False, ""]:
            return None
        return image


# Form for updating core User model data (first name, last name, email)


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        # Link the form to the User model

        model = User
        # Include only editable fields from the User model

        fields = ["first_name", "last_name", "email"]
