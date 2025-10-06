from django import forms
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
        label="Image", required=False
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
