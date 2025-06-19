from django.contrib import admin
from django.utils.html import format_html
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_preview", "condition_code", "condition_expression", "created_at")
    readonly_fields = ("icon_preview",)
    search_fields = ("name", "condition_code")
    list_filter = ("created_at",)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:contain;"/>', obj.icon.url)
        return "—"

