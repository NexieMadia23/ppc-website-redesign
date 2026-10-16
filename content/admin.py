from django.contrib import admin
from .models import (
    Article,
    ContactDetails,
    ContactFaq,
    ContactTopic,
    DirectoryOffice,
    EmergencyContact,
    Event,
    Notice,
    SafetyTip,
    Service,
)


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


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "digits", "order")
    list_editable = ("number", "digits", "order")
    search_fields = ("name", "number", "note")


@admin.register(DirectoryOffice)
class DirectoryOfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "order")
    list_editable = ("phone", "order")
    search_fields = ("name", "phone", "email", "note")


@admin.register(SafetyTip)
class SafetyTipAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    search_fields = ("title", "body")


@admin.register(ContactTopic)
class ContactTopicAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(ContactFaq)
class ContactFaqAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)
    search_fields = ("question", "answer")


@admin.register(ContactDetails)
class ContactDetailsAdmin(admin.ModelAdmin):
    """The single contact row. Add once, then edit; never delete."""

    def has_add_permission(self, request):
        return not ContactDetails.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
