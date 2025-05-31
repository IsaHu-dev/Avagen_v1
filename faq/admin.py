from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # only set user on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
