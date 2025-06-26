import os
from django.core.management.base import BaseCommand
from products.models import DigitalProduct

# Base URL for Cloudinary where images are assumed to be hosted
CLOUDINARY_BASE_URL = (
    "https://res.cloudinary.com/your-cloud-name/image/upload/"
)


class Command(BaseCommand):
    # Help text shown when running `python manage.py help <command>`
    help = (
        'Update product image_url fields with Cloudinary URLs'
    )

    def handle(self, *args, **options):
        self.stdout.write('Starting to update product image URLs...')

        updated_count = 0
        total_products = DigitalProduct.objects.count()

        # Iterate over all products in the database
        for product in DigitalProduct.objects.all():
            # Only update if the product has an image but no image_url
            if product.image and not product.image_url:
                # Extract the filename from the image path
                filename = os.path.basename(str(product.image))
                
                # Construct the Cloudinary URL
                cloudinary_url = f"{CLOUDINARY_BASE_URL}{filename}"
                
                # Update the product's image_url field
                product.image_url = cloudinary_url
                product.save()
                
                updated_count += 1
                self.stdout.write(
                    f'Updated {product.name}: {cloudinary_url}'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} out of '
                f'{total_products} products'
            )
        )
