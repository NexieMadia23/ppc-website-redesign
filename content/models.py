import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_image_size(f):
    """Keep uploads small: free tier has only 512 MiB total."""
    if f.size > 2 * 1024 * 1024:
        raise ValidationError("Image must be 2 MB or smaller.")


def validate_link(value):
    """Every link is either an internal path or a real https address.

    Staging domains are rejected here as well as in Service.clean(), so a
    tempmain.puertoprincesa.ph URL cannot be saved through the admin either.
    """
    url = (value or "").strip()
    if "tempmain" in url or "staging" in url:
        raise ValidationError("Staging URLs are not allowed.")
    if not (url.startswith("/") or url.startswith("https://")):
        raise ValidationError(
            "Use '/' for an internal page or a full 'https://' address for an external site."
        )


class AltTextMixin(models.Model):
    """Shared rule: an image can't be saved without alt text."""
    image = models.ImageField(
        upload_to="images/%Y/%m/", blank=True, validators=[validate_image_size]
    )
    image_alt = models.CharField(
        max_length=200, blank=True,
        help_text="Describe what the image shows, for screen reader users. "
                  "Required whenever an image is uploaded.",
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.image and not self.image_alt.strip():
            raise ValidationError({"image_alt": "Alt text is required when an image is uploaded."})


class ArticleQuerySet(models.QuerySet):
    """Everything the public site may show from the newsroom."""

    def published(self):
        """Future-dated articles stay hidden until their date arrives."""
        return self.filter(published_at__lte=timezone.now())


class Article(AltTextMixin):
    """A story from the City Information Office.

    `category` is the CIO's own section - the chip shown on the card - not a
    content type: the live site files stories under City government, City
    Council, Tourism, and Health.
    """

    class Category(models.TextChoices):
        CITY_GOVERNMENT = "city-government", "City government"
        CITY_COUNCIL = "city-council", "City Council"
        TOURISM = "tourism", "Tourism"
        HEALTH = "health", "Health"
        ADVISORY = "advisory", "Advisory"
        PRESS = "press", "Press release"
        ANNOUNCEMENT = "announcement", "Announcement"

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        FILIPINO = "fil", "Filipino"

    title = models.CharField(max_length=200, help_text="Use sentence case, not ALL CAPS.")
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300, help_text="One or two sentences for news cards.")
    body = models.TextField(
        help_text="One blank line between paragraphs: each block becomes its own paragraph on the page."
    )
    author = models.CharField(
        max_length=150, blank=True,
        help_text="Byline, e.g. 'Charlito Christopher Padul, CIO'.",
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.CITY_GOVERNMENT
    )
    language = models.CharField(max_length=3, choices=Language.choices, default=Language.ENGLISH)
    published_at = models.DateTimeField(
        default=timezone.now,
        help_text="Future dates keep the article hidden until then.",
    )

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    @property
    def date(self):
        """Date-only form of published_at: the templates render `article.date`."""
        return self.published_at.date()

    @property
    def paragraphs(self):
        """Body split into paragraphs: the template loops over `article.paragraphs`."""
        return [chunk.strip() for chunk in re.split(r"\n\s*\n", self.body or "") if chunk.strip()]


class EventQuerySet(models.QuerySet):
    """Everything the public site may show as upcoming."""

    def upcoming(self):
        """Events that have not started yet."""
        return self.filter(start_datetime__gte=timezone.now())


class Event(AltTextMixin):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(
        blank=True,
        help_text="Optional. Shown wherever the event is described in full.",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)
    contact = models.CharField(max_length=200, blank=True, help_text="Phone or email for inquiries.")
    url = models.CharField(
        max_length=300, blank=True, validators=[validate_link],
        help_text="Page about this event. Leave blank if there is not one yet: "
                  "the listing then shows the title without a link.",
    )

    class Meta:
        ordering = ["start_datetime"]

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} ({self.start_datetime:%Y-%m-%d})"

    def clean(self):
        super().clean()
        if self.end_datetime and self.start_datetime and self.end_datetime < self.start_datetime:
            raise ValidationError({"end_datetime": "End must be after the start."})

    @property
    def date(self):
        """Date-only form of start_datetime: the templates render `event.date`."""
        return self.start_datetime.date()

    @property
    def time(self):
        """Clock time as the templates render it, e.g. '6:00 AM'."""
        return self.start_datetime.strftime("%I:%M %p").lstrip("0")


class Notice(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    body = models.TextField(
        blank=True,
        help_text="Optional: a notice may be only a title and a link to a document.",
    )
    url = models.CharField(
        max_length=300, blank=True, validators=[validate_link],
        help_text="Document or page behind this notice. Leave blank if there is none yet: "
                  "the listing then shows the title without a link.",
    )
    published_at = models.DateTimeField(default=timezone.now)
    is_urgent = models.BooleanField(default=False, help_text="Urgent notices are highlighted on the homepage.")

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

    class Section(models.TextChoices):
        # The homepage shows two groups of the same kind of thing: the top row
        # of quick e-Portals, then the individual city offices and attractions.
        PORTALS = "portals", "e-Portal"
        OFFICES = "offices", "City services and offices"

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Symbol name from the icon sprite (templates/partials/icons.html), "
                  "e.g. 'credit-card', 'file-text', 'phone'.",
    )
    url = models.CharField(
        max_length=300, validators=[validate_link],
        help_text="Internal page: start with '/' (e.g. /residents/permits/). "
                  "External site: full https:// address.",
    )
    is_external = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=100, help_text="Lower numbers appear first.")
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.RESIDENTS)
    section = models.CharField(
        max_length=10, choices=Section.choices, default=Section.OFFICES,
        help_text="Which homepage group this belongs to.",
    )

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
