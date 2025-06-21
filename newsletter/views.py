from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterForm

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "This email is already subscribed or invalid.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
