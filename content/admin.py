from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import (
    Agency,
    Article,
    Complaint,
    ComplaintAttachment,
    ComplaintUpdate,
    ContactMessage,
    Document,
    Event,
    Feedback,
    Notice,
    Office,
    Service,
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "language", "published_at", "is_live")
    list_filter = ("category", "language", "published_at")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    actions = ("publish_now", "unpublish")

    @admin.display(boolean=True, description="Published")
    def is_live(self, obj):
        return obj.is_published

    @admin.action(description="Publish selected articles now")
    def publish_now(self, request, queryset):
        updated = queryset.update(published_at=timezone.now())
        self.message_user(request, f"{updated} article(s) published.")

    @admin.action(description="Move selected articles back to draft")
    def unpublish(self, request, queryset):
        updated = queryset.update(published_at=timezone.now() + timedelta(days=3650))
        self.message_user(request, f"{updated} article(s) moved to draft.")


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


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "email", "phone", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("name", "description", "email")


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "agency", "phone", "is_emergency", "order")
    list_editable = ("order",)
    list_filter = ("is_emergency", "agency")
    search_fields = ("name", "description", "address", "email")
    filter_horizontal = ("services",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "is_public", "published_at")
    list_filter = ("category", "year", "is_public")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


class ComplaintAttachmentInline(admin.TabularInline):
    model = ComplaintAttachment
    extra = 0
    readonly_fields = ("original_name", "content_type", "size", "created_at")


class ComplaintUpdateInline(admin.TabularInline):
    model = ComplaintUpdate
    extra = 0
    readonly_fields = ("created_at", "created_by")


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "subject",
        "barangay",
        "category",
        "agency",
        "status",
        "created_at",
    )
    list_filter = ("status", "category", "barangay", "agency", "created_at")
    search_fields = (
        "reference",
        "subject",
        "details",
        "barangay",
        "landmark",
        "name",
        "email",
        "phone",
    )
    readonly_fields = ("reference", "created_at", "updated_at", "resolved_at")
    date_hierarchy = "created_at"
    inlines = (ComplaintAttachmentInline, ComplaintUpdateInline)
    autocomplete_fields = ("agency", "assigned_to")

    def save_model(self, request, obj, form, change):
        if not obj.assigned_to and request.user.is_staff:
            obj.assigned_to = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ("complaint", "status", "created_by", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("complaint__reference", "complaint__subject", "note")
    readonly_fields = ("created_at",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("page", "helpful", "is_reviewed", "created_at")
    list_filter = ("helpful", "is_reviewed", "created_at")
    search_fields = ("page", "comment")
    list_editable = ("is_reviewed",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "email", "is_reviewed", "created_at")
    list_filter = ("is_reviewed", "topic", "created_at")
    search_fields = ("name", "email", "phone", "topic", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_reviewed",)
    date_hierarchy = "created_at"
