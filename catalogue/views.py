from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import DigitalProduct
from checkout.models import Order
from .models import DigitalDownload


def catalogue(request):
    """
    View to display the catalogue of available products
    """
    products = DigitalProduct.objects.filter(status="published").order_by(
        "-date_created"
    )
    context = {
        "products": products,
    }
    return render(request, "catalogue/catalogue.html", context)


@login_required
def download_file(request, product_id):
    """
    View to handle digital file downloads - only for users who purchased
    the product
    """
    product = get_object_or_404(DigitalProduct, id=product_id)

    # Check if the product has a digital download

    try:
        digital_download = DigitalDownload.objects.get(product=product)
    except DigitalDownload.DoesNotExist:
        raise Http404("No digital download found for this product")

    user_orders = Order.objects.filter(
        user=request.user,
        stripe_pid__isnull=False,  # Only paid orders
        lineitems__product=product,
    ).exists()

    if not user_orders:
        messages.error(
            request, "You need to purchase this product to download it."
        )
        return redirect("products")
    # Return the file for download

    return FileResponse(digital_download.file, as_attachment=True)
