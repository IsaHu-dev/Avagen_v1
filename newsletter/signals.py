from django.db.models.signals import post_save  # This is a built-in Django signal that runs after something is saved in the database
from django.dispatch import receiver  # This lets us connect our function to the signal
from django.core.mail import send_mail  # This is used to send emails
from django.template.loader import render_to_string  # This helps us fill in email templates
from django.conf import settings  # This gives us access to email settings
from .models import NewsletterSubscriber  # This is our subscriber model

# This decorator tells Django:
# "Whenever a new NewsletterSubscriber is saved, run the function below."
@receiver(post_save, sender=NewsletterSubscriber)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    """
    When someone signs up for the newsletter, this function sends them a welcome email.
    It only runs when a new subscriber is created (not when an existing one is updated).
    """
    if created:  # Only do this if it's a new subscriber
        try:
            # Prepare the information to fill in the email templates
            context = {
                'subscriber': instance,  # The new subscriber
                'welcome_message': (
                    f"Welcome to Avagen, {instance.first_name or 'there'}! 🎉\n\n"
                    "Thank you for subscribing to our newsletter. You'll now "
                    "receive updates about our latest digital products, "
                    "special offers, and exclusive content.\n\n"
                    "What you can expect:\n"
                    "• New product announcements\n"
                    "• Special discounts and offers\n"
                    "• Community updates\n\n"
                    "We're excited to have you as part of our community!"
                )
            }
            
            # Fill in the plain text and HTML email templates with the subscriber's info
            text_content = render_to_string(
                'newsletter/email/welcome_email.txt', 
                context
            )
            html_content = render_to_string(
                'newsletter/email/welcome_email.html', 
                context
            )
            
            # Send the welcome email to the new subscriber
            send_mail(
                subject='Welcome to Avagen Newsletter! 🎉',
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                html_message=html_content,
                fail_silently=True,  # Don't crash if the email can't be sent
            )
            
            print(f"Welcome email sent to {instance.email}")  # For debugging
            
        except Exception as e:
            # If something goes wrong, print an error message (for debugging)
            print(f"Failed to send welcome email to {instance.email}: {e}") 