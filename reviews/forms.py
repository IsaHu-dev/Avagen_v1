from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'star-rating-input'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Share your experience with this product...'
                }
            )
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in range(1, 6):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating 