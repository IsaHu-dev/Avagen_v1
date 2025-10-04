"""
Custom signal handlers for the Avagen project
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import email_confirmed, password_reset
import logging

logger = logging.getLogger(__name__)


@receiver(email_confirmed)
def email_confirmed_handler(sender, request, email_address, **kwargs):
    """Handle email confirmation"""
    logger.info(f"Email confirmed for user: {email_address.user.username}")


@receiver(password_reset)
def password_reset_handler(sender, request, user, **kwargs):
    """Handle password reset"""
    logger.info(f"Password reset requested for user: {user.username}")
