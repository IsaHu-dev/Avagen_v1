from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, CustomUserUpdateForm


@login_required
def profile(request):
    """Display the user's profile."""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        
        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_form.save()
                # Refresh the profile object to get updated data
                profile.refresh_from_db()
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(
                    request, f'Error saving profile: {str(e)}'
                )
        else:
            # Show specific form errors
            if not user_form.is_valid():
                messages.error(
                    request, 
                    'User information has errors. Please check the form.'
                )
            if not profile_form.is_valid():
                messages.error(
                    request, 
                    'Profile information has errors. Please check the form.'
                )
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    orders = profile.user.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'profile': profile,  # Explicitly pass profile to context
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)
