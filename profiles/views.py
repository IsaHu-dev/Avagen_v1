from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile(request):
    """
    Display the user's profile and allow updates via a form.
    Also fetch and display the user's past orders.
    """
    # Get or create the UserProfile object for the currently logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # If the form has been submitted (POST request)
    if request.method == 'POST':
        # Populate form with POST data and bind it to the existing profile
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save the updated profile data
            form.save()
            # Display a success message to the user
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:  # If not POST, display the form pre-filled with existing profile data
        form = UserProfileForm(instance=profile)

    # Retrieve all orders associated with this user profile
    orders = profile.orders.all()

    # Render the profile page with the form and order list
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True  # Optional context variable that may be used for conditional display in the template
    }

    return render(request, template, context)
