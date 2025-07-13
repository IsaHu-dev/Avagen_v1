from django.db.models.signals import post_save  # Signal after saving in DB
from django.dispatch import receiver  # Connects a function to a signal
from django.core.mail import send_mail  # Used to send emails
from django.template.loader import render_to_string  # Renders email templates
from django.conf import settings  # Access Django settings
from .models import NewsletterSubscriber  # Newsletter model


@receiver(post_save, sender=NewsletterSubscriber)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    """
    Sends a welcome email when a new newsletter subscriber is created.
    """
    if created:
        try:
            context = {
                'subscriber': instance,
                'welcome_message': (
                    f"Welcome to Avagen, {instance.first_name or 'there'}!\n\n"
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

            text_content = render_to_string(
                'newsletter/email/welcome_email.txt',
                context
            )
            html_content = render_to_string(
                'newsletter/email/welcome_email.html',
                context
            )

            send_mail(
                subject='Welcome to Avagen Newsletter! 🎉',
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                html_message=html_content,
                fail_silently=True,
            )

            print(
                f"Welcome email sent to {instance.email}"
            )

        except Exception as e:
            print(
                f"Failed to send welcome email to {instance.email}: {e}"
            )
