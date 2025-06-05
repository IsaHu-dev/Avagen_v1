from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):
    help = 'Updates the site domain for email verification'

    def handle(self, *args, **options):
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = settings.SITE_DOMAIN
        site.name = 'Avagen'
        site.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated site domain to {settings.SITE_DOMAIN}')) 