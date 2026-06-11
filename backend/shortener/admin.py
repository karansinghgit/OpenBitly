from django.contrib import admin

from .models import Click, Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("code", "long_url", "created_at")
    search_fields = ("code", "long_url")


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ("link", "created_at", "referer")
    list_filter = ("created_at",)
