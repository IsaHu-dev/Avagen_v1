from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import UserProfile
from .forms import UserProfileForm, CustomUserUpdateForm
from catalogue.models import DigitalDownload


@login_required
def profile(request):
    """Display the user's profile."""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if created:
        messages.info(request, 'Profile created successfully!')

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        
        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_instance = profile_form.save(commit=False)
                if not request.FILES.get('profile_image'):
                    profile_instance.profile_image = profile.profile_image
                profile_instance.save()
                # Refresh the profile object to get updated data
                profile.refresh_from_db()
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(
                    request,
                    'Error saving profile: '
                    f'{str(e)}'
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
    
    # Get user's orders ordered by date (newest first)
    orders = request.user.orders.all().order_by('-date')
    
    # Get digital downloads for purchased products
    # This creates a list of all digital products the user has purchased
    purchased_products = []
    for order in orders:
        for line_item in order.lineitems.all():
            try:
                # Try to get the digital download file for this product
                digital_download = line_item.product.digital_download
                # Add product info to the list if download file exists
                purchased_products.append({
                    'product': line_item.product,
                    'download': digital_download,
                    'license_type': line_item.license_type,
                    'order_date': order.date,
                    'order_number': order.order_number
                })
            except DigitalDownload.DoesNotExist:
                # Product doesn't have a digital download file
                continue

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
        'purchased_products': purchased_products,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def delete_account(request):
    """Handle account deletion with confirmation."""
    if request.method == 'POST':
        # Check if user confirmed deletion
        if 'confirm_delete' in request.POST:
            try:
                # Get user data for confirmation message
                username = request.user.username
                email = request.user.email
                
                # Delete the user (this will cascade to profile and related data)
                request.user.delete()
                
                # Logout the user
                logout(request)
                
                messages.success(
                    request, 
                    f'Account for {username} ({email}) has been '
                    f'permanently deleted.'
                )
                return redirect('home')
            except Exception as e:
                messages.error(
                    request, 
                    f'Error deleting account: '
                    f'{str(e)}'
                )
        else:
            messages.warning(
                request, 
                'Account deletion cancelled.'
            )
            return redirect('profile')
    
    # GET request - show confirmation page
    return render(
        request, 
        'profiles/delete_account.html', 
        {'on_profile_page': True}
    )
