from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        # add model_number field for superusers or staff
        if user and (user.is_superuser or user.is_staff):
            self.fields['model_number'] = forms.CharField(required=False)
        else:
            self.fields.pop('model_number', None)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
        }
