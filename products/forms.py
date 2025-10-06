from django import forms
from django.core.exceptions import ValidationError
from .widgets import CustomClearableFileInput
from .models import DigitalProduct, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = DigitalProduct
        fields = [
            "name",
            "description",
            "category",
            "base_price",
            "image",
            "image_url",
            "model_number",
            "status",
        ]

    image = forms.ImageField(
        label="Product Image", 
        required=False, 
        widget=CustomClearableFileInput,
        help_text="Upload an image file (JPG, PNG, WEBP, GIF). Max size: 5MB, Dimensions: 100x100px to 500x500px"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Extract the user
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields["category"].choices = friendly_names

        # add model_number field for superusers or staff

        if user and (user.is_superuser or user.is_staff):
            self.fields["model_number"] = forms.CharField(required=False)
        else:
            self.fields.pop("model_number", None)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded-0"
    
    def clean_image(self):
        """Validate image file format, size, and dimensions"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise ValidationError(
                    "Image file is too large. Maximum size allowed is 5MB. "
                    "Please compress your image or choose a smaller file."
                )
            
            # Check file format and dimensions
            allowed_formats = ['JPEG', 'JPG', 'PNG', 'WEBP', 'GIF']
            
            try:
                # Try to open and validate the image
                if hasattr(image, 'image'):
                    img = image.image
                    format_name = img.format
                    
                    # Check format
                    if format_name not in allowed_formats:
                        raise ValidationError(
                            f"Invalid image format. Please upload a file in one of these formats: "
                            f"{', '.join(allowed_formats)}. "
                            f"You uploaded a {format_name} file."
                        )
                    
                    # Check image dimensions
                    width, height = img.size
                    max_width, max_height = 500, 500  # Maximum dimensions
                    min_width, min_height = 100, 100    # Minimum dimensions
                    
                    if width > max_width or height > max_height:
                        raise ValidationError(
                            f"Image dimensions are too large. Maximum allowed: {max_width}x{max_height}px. "
                            f"Your image: {width}x{height}px. Please resize your image."
                        )
                    
                    if width < min_width or height < min_height:
                        raise ValidationError(
                            f"Image dimensions are too small. Minimum required: {min_width}x{min_height}px. "
                            f"Your image: {width}x{height}px. Please use a higher resolution image."
                        )
                    
                    # Check if image is corrupted or incompatible
                    try:
                        img.verify()
                    except Exception as e:
                        raise ValidationError(
                            f"Image file appears to be corrupted or incompatible. "
                            f"Please try a different image file. Error: {str(e)}"
                        )
                        
            except ValidationError:
                # Re-raise validation errors
                raise
            except Exception as e:
                # Handle other image-related errors
                file_name = image.name.lower()
                if not any(file_name.endswith(f'.{fmt.lower()}') for fmt in allowed_formats):
                    raise ValidationError(
                        f"Invalid file type. Please upload an image file with one of these extensions: "
                        f"{', '.join([f'.{fmt.lower()}' for fmt in allowed_formats])}. "
                        f"Your file: {image.name}"
                    )
                else:
                    raise ValidationError(
                        f"Image size is not compatible. The file may be corrupted or in an unsupported format. "
                        f"Please try uploading a different image file. "
                        f"Supported formats: {', '.join(allowed_formats)}"
                    )
        
        return image
