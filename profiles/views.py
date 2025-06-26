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
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.'
            )
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    orders = profile.user.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)
