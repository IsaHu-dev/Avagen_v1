from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Check current email settings'

    def handle(self, *args, **options):
        self.stdout.write("Current Email Settings:")
        self.stdout.write(
            f"EMAIL_HOST_USER: "
            f"{getattr(settings, 'EMAIL_HOST_USER', 'Not set')}"
        )
        self.stdout.write(
            f"DEFAULT_FROM_EMAIL: "
            f"{getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}"
        )
        self.stdout.write(
            f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}"
        )
        self.stdout.write(
            f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}"
        )
        self.stdout.write(
            f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}"
        )
        self.stdout.write(
            f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}"
        )
        
        # Check environment variables
        import os
        self.stdout.write("\nEnvironment Variables:")
        self.stdout.write(
            f"EMAIL_HOST_USER (env): "
            f"{os.environ.get('EMAIL_HOST_USER', 'Not set')}"
        )
        self.stdout.write(
            f"EMAIL_HOST_PASSWORD (env): "
            f"{'Set' if os.environ.get('EMAIL_HOST_PASSWORD') else 'Not set'}"
        ) 