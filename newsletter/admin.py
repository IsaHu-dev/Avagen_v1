from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'subscribed_at', 'is_active'
    ]
    list_filter = ['subscribed_at', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['subscribed_at']
    ordering = ['-subscribed_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('email', 'first_name', 'last_name')
        }),
        ('Subscription Details', {
            'fields': ('is_active', 'subscribed_at'),
            'classes': ('collapse',)
        }),
    )
