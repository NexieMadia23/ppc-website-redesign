from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .constants import BARANGAY_CHOICES, COMPLAINT_SLA_DAYS

ATTACHMENT_MAX_BYTES = 5 * 1024 * 1024
ATTACHMENT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_size(f):
    """Keep uploads small: free tier has only 512 MiB total."""
    if f.size > 2 * 1024 * 1024:
        raise ValidationError("Image must be 2 MB or smaller.")


def validate_document_size(f):
    """Transparency documents are PDFs; keep the free-tier disk in mind."""
    if f.size > 10 * 1024 * 1024:
        raise ValidationError("Document must be 10 MB or smaller.")


def validate_attachment_size(f):
    if f.size > ATTACHMENT_MAX_BYTES:
        raise ValidationError("Each photo must be 5 MB or smaller.")


def validate_attachment_type(f):
    suffix = Path(f.name or "").suffix.lower()
    if suffix not in ATTACHMENT_EXTENSIONS:
        raise ValidationError("Upload a JPG, PNG, or WebP photo.")


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


class ArticleQuerySet(models.QuerySet):
    """Published articles only: future-dated drafts stay hidden everywhere."""

    def published(self):
        return self.filter(published_at__lte=timezone.now())


class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    pass


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

    objects = ArticleManager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", args=[self.slug])

    @property
    def is_published(self):
        return self.published_at <= timezone.now()


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

    def get_absolute_url(self):
        return reverse("event_detail", args=[self.slug])

    def clean(self):
        super().clean()
        if self.end_datetime and self.start_datetime and self.end_datetime < self.start_datetime:
            raise ValidationError({"end_datetime": "End must be after the start."})


class Notice(AltTextMixin):
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

    def get_absolute_url(self):
        return reverse("notice_detail", args=[self.slug])


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


class Agency(models.Model):
    """A city department that receives routed complaints."""

    class Category(models.TextChoices):
        INFRASTRUCTURE = "infrastructure", "Infrastructure"
        SANITATION = "sanitation", "Sanitation and waste"
        HEALTH = "health", "Health"
        SAFETY = "safety", "Peace, safety, and traffic"
        BUSINESS = "business", "Business and permits"
        ENVIRONMENT = "environment", "Environment"
        SOCIAL = "social", "Social services"
        OTHER = "other", "Other concerns"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    description = models.CharField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.name


class Office(models.Model):
    """A public office in the city directory."""

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    agency = models.ForeignKey(
        Agency,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="offices",
    )
    description = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=240, blank=True)
    hours = models.CharField(
        max_length=160,
        default="Mondays to Fridays, 8:00 AM to 5:00 PM",
    )
    phone = models.CharField(max_length=40, blank=True)
    phone_digits = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    is_emergency = models.BooleanField(default=False)
    services = models.ManyToManyField(Service, blank=True, related_name="offices")
    order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def tel_href(self):
        digits = self.phone_digits or self.phone
        return "tel:" + "".join(ch for ch in digits if ch.isdigit() or ch == "+")


class Document(models.Model):
    """A downloadable transparency or FOI document."""

    class Category(models.TextChoices):
        BUDGET = "budget", "Budget and finance"
        BIDS = "bids", "Bids and awards"
        ORDINANCE = "ordinance", "Ordinances and resolutions"
        REPORT = "report", "Reports"
        FOI = "foi", "Freedom of information"
        OTHER = "other", "Other documents"

    class Status(models.TextChoices):
        PUBLISHED = "published", "Published"
        FOR_RELEASE = "for_release", "For release"
        ON_REQUEST = "on_request", "On request"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    year = models.PositiveSmallIntegerField(default=timezone.now().year)
    description = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        help_text="Only Published documents need a file or link. For release "
        "means the document is approved and the signed copy is being prepared.",
    )
    file = models.FileField(
        upload_to="documents/%Y/", blank=True, validators=[validate_document_size]
    )
    external_url = models.URLField(
        blank=True, help_text="Use when the document lives on another official site."
    )
    published_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year", "-published_at", "title"]

    def __str__(self):
        return f"{self.title} ({self.year})"

    def clean(self):
        super().clean()
        if self.status == self.Status.PUBLISHED and not (self.file or self.external_url):
            raise ValidationError("Published documents need a file or an external URL.")

    @property
    def is_available(self):
        return bool(self.file or self.external_url)

    @property
    def href(self):
        if self.file:
            return self.file.url
        return self.external_url


class Complaint(models.Model):
    """A Sumbungan ng Bayan request routed to a city agency."""

    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        IN_REVIEW = "in_review", "In review"
        REFERRED = "referred", "Referred to agency"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class Category(models.TextChoices):
        INFRASTRUCTURE = "infrastructure", "Infrastructure"
        SANITATION = "sanitation", "Sanitation and waste"
        HEALTH = "health", "Health"
        SAFETY = "safety", "Peace, safety, and traffic"
        BUSINESS = "business", "Business and permits"
        ENVIRONMENT = "environment", "Environment"
        SOCIAL = "social", "Social services"
        OTHER = "other", "Other concerns"

    reference = models.CharField(max_length=24, unique=True, blank=True, editable=False)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    agency = models.ForeignKey(
        Agency,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="complaints",
    )
    subject = models.CharField(max_length=200)
    details = models.TextField()
    barangay = models.CharField(
        max_length=80,
        choices=BARANGAY_CHOICES,
        blank=True,
        db_index=True,
        help_text="The barangay where the concern happened.",
    )
    landmark = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional landmark or street to help the team find it.",
    )
    name = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    is_anonymous = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_complaints",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["category"]),
            models.Index(fields=["barangay"]),
        ]

    def __str__(self):
        return f"{self.reference or 'new'} - {self.subject}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.reference:
            year = self.created_at.year if self.created_at else timezone.now().year
            self.reference = f"PPC-{year}-{self.pk:06d}"
            super().save(update_fields=["reference"])

    def get_absolute_url(self):
        return reverse("complaint_track_detail", args=[self.reference])

    @property
    def sla_days(self):
        return COMPLAINT_SLA_DAYS.get(self.category, 7)

    @property
    def due_at(self):
        return self.created_at + timedelta(days=self.sla_days)

    @property
    def is_overdue(self):
        if self.status in {self.Status.RESOLVED, self.Status.CLOSED}:
            return False
        return timezone.now() > self.due_at

    def clean(self):
        super().clean()
        if not self.is_anonymous and not (self.name and (self.email or self.phone)):
            raise ValidationError(
                "Provide a name and at least one contact detail, or choose to stay anonymous."
            )
        if not self.consent:
            raise ValidationError({"consent": "Consent is required to submit a complaint."})


class ComplaintAttachment(models.Model):
    """A photo uploaded with a request.

    Images are re-encoded as WebP on upload so EXIF/GPS metadata never reaches
    the server's public media directory.
    """

    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(
        upload_to="complaints/%Y/%m/",
        validators=[validate_attachment_size, validate_attachment_type],
    )
    original_name = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.original_name or Path(self.file.name).name


class ComplaintUpdate(models.Model):
    """An audited status change or note on a complaint."""

    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="updates")
    status = models.CharField(max_length=20, choices=Complaint.Status.choices)
    note = models.TextField(blank=True)
    is_public = models.BooleanField(
        default=True,
        help_text="Untick for an internal note that residents must not see.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="complaint_updates",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.complaint.reference}: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update = {"status": self.status}
        if self.status == Complaint.Status.RESOLVED:
            update["resolved_at"] = timezone.now()
        Complaint.objects.filter(pk=self.complaint_id).update(**update)


class Feedback(models.Model):
    """A quick 'was this page helpful?' response."""

    page = models.CharField(max_length=200)
    helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "feedback"

    def __str__(self):
        return f"{self.page}: {'helpful' if self.helpful else 'not helpful'}"


class ContactMessage(models.Model):
    """A message sent through the public contact form."""

    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    topic = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"

    def __str__(self):
        return f"{self.name} - {self.topic or 'General inquiry'}"


class FaqQuery(models.Model):
    """An assistant question the FAQ could not answer.

    Only unanswered questions are stored. That keeps the log small, avoids
    keeping personal data for no reason, and gives the content team a direct
    list of gaps to write answers for. Questions are trimmed to 500 characters
    and automatically removed by ``purge_expired_data``.
    """

    question = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "unanswered assistant question"
        verbose_name_plural = "unanswered assistant questions"

    def __str__(self):
        return self.question

