from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Category

# Create your views here.

def all_products(request):
    """
    View to display all products with filtering, sorting, and search functionality
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    current_category = None
    current_sorting = None

    # Handle search query
    if 'q' in request.GET:
        query = request.GET['q'].strip()
        if query:
            search_queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(search_queries)
        else:
            messages.warning(request, "Please enter a search term.")
            return redirect(reverse('products'))

    # Handle category filtering
    if 'category' in request.GET:
        category_name = request.GET['category']
        try:
            current_category = Category.objects.get(friendly_name=category_name)
            products = products.filter(category=current_category)
        except Category.DoesNotExist:
            messages.error(request, f"Category '{category_name}' not found.")
            return redirect(reverse('products'))

    # Handle sorting
    if 'sort' in request.GET and 'direction' in request.GET:
        sort = request.GET['sort']
        direction = request.GET['direction']
        current_sorting = f"{sort}_{direction}"

        if sort == 'price':
            products = products.order_by(f"{'-' if direction == 'desc' else ''}price")
        elif sort == 'rating':
            products = products.annotate(avg_rating=Avg('rating')).order_by(
                f"{'-' if direction == 'desc' else ''}avg_rating"
            )
        elif sort == 'name':
            products = products.order_by(f"{'-' if direction == 'desc' else ''}name")
        else:
            messages.error(request, "Invalid sorting option.")
            return redirect(reverse('products'))

    # Add rating and review count to products
    products = products.annotate(
        avg_rating=Avg('rating'),
        review_count=Count('rating')
    )

    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': current_category,
        'current_sorting': current_sorting,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect(reverse('product_detail', args=[product_id]))
    else:
        review_form = ReviewForm()

    # Calculate average rating, defaulting to 0 if no ratings exist
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': avg_rating,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
