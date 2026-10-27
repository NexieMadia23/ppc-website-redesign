from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_image_size(f):
    """Keep uploads small: free tier has only 512 MiB total."""
    if f.size > 2 * 1024 * 1024:
        raise ValidationError("Image must be 2 MB or smaller.")


class AltTextMixin(models.Model):
    """Shared rule: an image can't be saved without alt text."""

    image = models.ImageField(
        upload_to="images/%Y/%m/", blank=True, validators=[validate_image_size]
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Describe what the image shows, for screen reader users. "
        "Required whenever an image is uploaded.",
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.image and not self.image_alt.strip():
            raise ValidationError({"image_alt": "Alt text is required when an image is uploaded."})


class Article(AltTextMixin):
    class Category(models.TextChoices):
        NEWS = "news", "News"
        ADVISORY = "advisory", "Advisory"
        PRESS = "press", "Press release"
        ANNOUNCEMENT = "announcement", "Announcement"

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        FILIPINO = "fil", "Filipino"

    title = models.CharField(max_length=200, help_text="Use sentence case, not ALL CAPS.")
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300, help_text="One or two sentences for news cards.")
    body = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.NEWS)
    language = models.CharField(max_length=3, choices=Language.choices, default=Language.ENGLISH)
    published_at = models.DateTimeField(
        default=timezone.now,
        help_text="Future dates keep the article hidden until then.",
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Event(AltTextMixin):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)
    contact = models.CharField(
        max_length=200, blank=True, help_text="Phone or email for inquiries."
    )

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return f"{self.title} ({self.start_datetime:%Y-%m-%d})"

    def clean(self):
        super().clean()
        if self.end_datetime and self.start_datetime and self.end_datetime < self.start_datetime:
            raise ValidationError({"end_datetime": "End must be after the start."})


class Notice(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    body = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    is_urgent = models.BooleanField(
        default=False, help_text="Urgent notices are highlighted on the homepage."
    )

    class Meta:
        ordering = ["-is_urgent", "-published_at"]

    def __str__(self):
        return self.title


class Service(models.Model):
    class Audience(models.TextChoices):
        RESIDENTS = "residents", "Residents"
        BUSINESS = "business", "Business"
        VISITORS = "visitors", "Visitors"
        ALL = "all", "Everyone"

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide icon name, e.g. 'credit-card', 'file-text', 'phone'.",
    )
    url = models.CharField(
        max_length=300,
        help_text="Internal page: start with '/' (e.g. /residents/permits/). "
        "External site: full https:// address.",
    )
    is_external = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=100, help_text="Lower numbers appear first.")
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.RESIDENTS)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        url = (self.url or "").strip()
        if self.is_external and not url.startswith("https://"):
            raise ValidationError({"url": "External links must start with https://"})
        if not self.is_external and not url.startswith("/"):
            raise ValidationError({"url": "Internal links must start with '/'."})
        if "tempmain" in url or "staging" in url:
            raise ValidationError({"url": "Staging URLs are not allowed."})
