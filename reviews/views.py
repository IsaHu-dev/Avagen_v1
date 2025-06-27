from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from products.models import DigitalProduct


@login_required
def add_review(request, product_id):
    """ Add a review to a product """
    product = get_object_or_404(DigitalProduct, pk=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.name = request.user.username
            review.product = product
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(
                request, 
                'Failed to add review. Please ensure the form is valid.'
            )
    else:
        form = ReviewForm()

    template = 'reviews/add_review.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
