# Written by Isa Hu

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Importing the UserProfile model and associated form
from .models import UserProfile
from .forms import UserProfileForm, CustomUserUpdateForm

# Import the Order model (from checkout app) to show user's order history
from checkout.models import Order

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

    # Retrieve all orders associated with this user
    orders = request.user.orders.all().order_by('-date')

    # Render the profile page with the forms and order list
    template = 'profiles/profile.html'
    context = {
        'profile': profile, # UserProfile object for displaying profile info
        'user_form': user_form,# Form for updating User model fields
        'profile_form': profile_form,# Form for updating UserProfile model
        'orders': orders, # User's order history
        'on_profile_page': True # Optional flag for use in templates
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Display a past order confirmation page from the user's order history.
    """
    # Safely fetch the Order by its number or return 404 if not found
    order = get_object_or_404(Order, order_number=order_number)

    # Notify the user that this is a historical confirmation
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    # Render the same template used for a successful checkout
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True
    }

    return render(request, template, context)
