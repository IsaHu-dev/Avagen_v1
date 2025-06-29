from django.contrib import admin
from .models import NewsletterSubscriber, Newsletter


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


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['title', 'subject', 'content']
    readonly_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']
    actions = ['send_newsletters']
    
    fieldsets = (
        ('Newsletter Content', {
            'fields': ('title', 'subject', 'content')
        }),
        ('Status & Statistics', {
            'fields': ('status', 'created_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )

    def send_newsletters(self, request, queryset):
        """Send selected newsletters to all active subscribers"""
        for newsletter in queryset:
            if newsletter.status == 'draft':
                try:
                    success_count = newsletter.send_newsletter()
                    self.message_user(
                        request,
                        f'Newsletter "{newsletter.title}" sent successfully to '
                        f'{success_count} subscribers.'
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f'Failed to send newsletter "{newsletter.title}": '
                        f'{str(e)}',
                        level='ERROR'
                    )
            else:
                self.message_user(
                    request,
                    f'Newsletter "{newsletter.title}" is not in draft status.',
                    level='WARNING'
                )
    
    send_newsletters.short_description = "Send selected newsletters"
