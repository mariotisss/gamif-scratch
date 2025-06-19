from django.contrib import admin
from .models import Mission, UserMission
from django.utils.html import format_html
from datetime import timedelta
import json

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "xp_reward", "is_active", "created_at", "display_expiration")
    list_filter = ("type", "is_active", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("display_expiration",)
    fieldsets = (
        (None, {
            "fields": (
                "title", "description", "type", "xp_reward", "is_active",
                "time_limit_days", "display_expiration", "metadata"
            )
        }),
    )

    def display_expiration(self, obj):
        exp = obj.expiration_date()
        return exp.strftime("%Y-%m-%d") if exp else "Sin límite"
    display_expiration.short_description = "Fecha de expiración"

    def formatted_metadata(self, obj):
        if not obj.metadata:
            return "—"
        return format_html("<pre>{}</pre>", json.dumps(obj.metadata, indent=2))

# --------------------------------------------

@admin.register(UserMission)
class UserMissionAdmin(admin.ModelAdmin):
    list_display = ("user", "mission", "completed_at", "mission_xp")
    list_filter = ("completed_at", "mission__type")
    search_fields = ("user__username", "mission__title")
    autocomplete_fields = ("user", "mission")
    readonly_fields = ("completed_at",)

    def mission_xp(self, obj):
        return obj.mission.xp_reward
    mission_xp.short_description = "XP otorgado"

