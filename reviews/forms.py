# reviews/forms.py
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': (
                    'Your first and last name'
                )
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with this product.',
                'rows': 4
            }),
            'rating': forms.RadioSelect(
                attrs={'class': 'form-check-input'},
                choices=[
                    (i, f'{i} Star{"s" if i > 1 else ""}')
                    for i in range(1, 6)
                ]
            ),
        }