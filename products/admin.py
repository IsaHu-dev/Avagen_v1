from django.contrib import admin
from .models import Product, Category, Review


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (

        'name',
        'category',
        'price',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
class CategoryCreatorAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'name',
        'created_at',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
