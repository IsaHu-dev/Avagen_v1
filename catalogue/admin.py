from django.contrib import admin
from django.utils.html import format_html
from .models import DigitalDownload


@admin.register(DigitalDownload)
class DigitalDownloadAdmin(admin.ModelAdmin):
    list_display = ("product", "uploaded_at", "download_link")
    readonly_fields = ("download_link",)
    fields = ("product", "file", "download_link", "uploaded_at")
    ordering = ("-uploaded_at",)

    def download_link(self, obj):
        if obj.file and obj.is_file_accessible():
            return format_html(
                '<a href="{}" target="_blank" download class="btn btn-sm btn-success">Download</a>',
                obj.file.url,
            )
        return format_html('<span class="text-danger">Not available</span>')

    download_link.short_description = "Download"
