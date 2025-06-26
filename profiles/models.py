from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
            )
        ],
        help_text=(
            'Upload a profile picture (JPG, PNG, GIF, WebP up to 5MB)'
        )
    )

    address_line_1 = models.CharField(
        "Address Line 1", max_length=255, blank=True
    )
    address_line_2 = models.CharField(
        "Address Line 2", max_length=255, blank=True
    )
    city = models.CharField("Town/City", max_length=100, blank=True)
    region = models.CharField("County/Region", max_length=100, blank=True)
    postal_code = models.CharField("Postcode", max_length=20, blank=True)
    country = CountryField(blank_label="(Select country)", blank=True)

    def __str__(self):
        return self.display_name or self.user.username
    
    def get_profile_image_url(self):
        """Return the profile image URL or default image if none exists"""
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return '/media/avatars/default.png'
