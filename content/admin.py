from django.contrib import admin
from .models import Article, Event, Notice, Service


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "language", "published_at")
    list_filter = ("category", "language", "published_at")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "venue")
    list_filter = ("start_datetime",)
    search_fields = ("title", "description", "venue")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"
    ordering = ("-start_datetime",)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "is_urgent", "published_at")
    list_filter = ("is_urgent", "published_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "audience", "order", "is_external", "url")
    list_editable = ("order",)
    list_filter = ("audience", "is_external")
    search_fields = ("name", "description")
