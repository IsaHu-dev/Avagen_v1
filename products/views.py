from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.db.models.functions import Lower, Coalesce

from .models import DigitalProduct, Category
from .forms import ProductForm
from reviews.forms import ReviewForm


def list_digital_products(request):
    """Display all products, with support for sorting, category filtering,
    and search."""

    items = DigitalProduct.objects.filter(status="published")
    active_query = None
    selected_categories = None
    sort_option = request.GET.get("sort", "")
    sorting_identifier = "None_None"

    # Handle sorting logic

    if sort_option:
        sorting_identifier = sort_option

        match sort_option:
            case "price_asc":
                items = items.order_by("base_price")
            case "price_desc":
                items = items.order_by("-base_price")
            case "name_az":
                items = items.annotate(lower_name=Lower("name")).order_by(
                    "lower_name"
                )
            case "name_za":
                items = items.annotate(lower_name=Lower("name")).order_by(
                    "-lower_name"
                )
            case "rating_high":
                items = items.annotate(
                    avg_score=Coalesce(Avg("reviews__rating"), 0.0)
                ).order_by("-avg_score", "name")
            case "rating_low":
                items = items.annotate(
                    avg_score=Coalesce(Avg("reviews__rating"), 0.0)
                ).order_by("avg_score", "name")
    # Category filter

    if "category" in request.GET:
        category_names = request.GET["category"].split(",")
        items = items.filter(category__name__in=category_names)
        selected_categories = Category.objects.filter(name__in=category_names)
    # Search query

    if "q" in request.GET:
        active_query = request.GET["q"]
        if not active_query.strip():
            messages.error(request, "Please enter a valid search term.")
            return redirect(reverse("products"))
        lookup = Q(name__icontains=active_query) | Q(
            description__icontains=active_query
        )
        items = items.filter(lookup)
    # Calculate average ratings and latest reviews for each product

    items = items.prefetch_related("reviews")

    context = {
        "products": items,
        "search_term": active_query,
        "current_categories": selected_categories,
        "current_sorting": sorting_identifier,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(DigitalProduct, pk=product_id)
    reviews = product.reviews.all().order_by("-created_at")

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect(reverse("product_detail", args=[product_id]))
    else:
        review_form = ReviewForm()
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    context = {
        "product": product,
        "reviews": reviews,
        "review_form": review_form,
        "avg_rating": avg_rating,
    }

    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to add product. Please ensure the form is valid.",
            )
    else:
        form = ProductForm()
    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit a product in the store"""
    product = get_object_or_404(DigitalProduct, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to update product. Please ensure the form is valid.",
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")
    template = "products/edit_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    product = get_object_or_404(DigitalProduct, pk=product_id)
    product.delete()
    messages.success(request, "Product deleted!")
    return redirect(reverse("products"))
