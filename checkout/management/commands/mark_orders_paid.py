"""
Management command to mark all orders as paid.
Useful for testing when webhooks aren't working properly.
"""

from django.core.management.base import BaseCommand
from checkout.models import Order


class Command(BaseCommand):
    help = 'Mark all orders as paid (useful for testing)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find all orders that are not paid
        orders_to_update = Order.objects.exclude(payment_status='paid')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Found {orders_to_update.count()} orders to update'
            )
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No changes will be made')
            )
            
            for order in orders_to_update:
                self.stdout.write(
                    f'Order {order.order_number}: '
                    f'Current Status: {order.payment_status}'
                )
        else:
            updated_count = orders_to_update.update(payment_status='paid')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {updated_count} orders to paid status'
                )
            )
