from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterForm


# This function is for the newsletter signup form at the bottom of the website.


def subscribe_newsletter(request):
    # If the form was submitted

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        # Check if the information entered is correct

        if form.is_valid():
            form.save()  # Save the new subscriber
            # Show a thank you message to the user

            messages.success(
                request, "Thanks for subscribing to our newsletter!"
            )
        else:
            # If an email is already used
            # show an error

            messages.error(
                request, "This email is already subscribed or invalid."
            )
        # After submitting, send the user back to the page they were on

        return redirect(request.META.get("HTTP_REFERER", "/"))
    # If the user didn't submit the form, send them to the home page

    return redirect("home")
