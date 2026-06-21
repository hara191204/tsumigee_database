from django.contrib import admin

from .models import Game, Hard, Maker


@admin.register(Maker)
class MakerAdmin(admin.ModelAdmin):
    list_display = ("name", "furigana", "created_at")
    search_fields = ("name", "furigana")
    ordering = ("furigana",)


@admin.register(Hard)
class HardAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "furigana",
        "maker",
        "hard",
        "play_hard",
        "clear_status",
        "grade",
        "is_package",
    )
    list_filter = ("clear_status", "grade", "hard", "is_package")
    search_fields = ("title", "furigana")
    ordering = ("furigana",)
    readonly_fields = ("created_at", "updated_at")
