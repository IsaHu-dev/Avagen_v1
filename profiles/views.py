# Written by Isa Hu

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Importing the UserProfile model and associated form
from .models import UserProfile
from .forms import UserProfileForm, CustomUserUpdateForm

# Import the DigitalPurchase model (from checkout app) to show user's purchase history
from checkout.models import DigitalPurchase

@login_required  # Ensure only logged-in users can access their profile
def profile(request):
    # Try to retrieve the UserProfile for the logged-in user;
    # if it doesn't exist yet, create a new one.
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # If this is a POST request, handle form submission
    if request.method == 'POST':
        # Populate forms with POST data
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, # Text fields from form
            request.FILES, # Image uploads, e.g. profile picture 
            instance=profile # Bind the form to the existing profile
        )

        # If both forms are valid, save the changes to DB
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Display a success message to the user
            messages.success(request, 'Profile updated successfully')
        else:
            # If there are errors, display them to the user
            messages.error(
                request, 
                'Update failed. Please ensure the form is valid.'
            )
    else:  # If not POST, display the forms pre-filled with existing data
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    # Retrieve all purchases associated with this user
    purchases = DigitalPurchase.objects.filter(customer=request.user).order_by('-created_at')

    # Render the profile page with the forms and purchase list
    template = 'profiles/profile.html'
    context = {
        'profile': profile, # UserProfile object for displaying profile info
        'user_form': user_form,# Form for updating User model fields
        'profile_form': profile_form,# Form for updating UserProfile model
        'purchases': purchases, # User's purchase history
        'on_profile_page': True # Optional flag for use in templates
    }

    return render(request, template, context)


def purchase_history_detail(request, purchase_id):
    """
    Display a past purchase confirmation page from the user's purchase history.
    """
    purchase = get_object_or_404(DigitalPurchase, purchase_id=purchase_id)
    if request.user.is_authenticated and purchase.customer != request.user:
        messages.error(request, 'Access denied')
        return redirect('profile')
    context = {
        'purchase': purchase,
        'purchase_items': purchase.purchase_items.all(),
    }
    return render(request, 'profiles/purchase_history_detail.html', context)
