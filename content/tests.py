"""Regression tests for the content app.

These cover the rules the project promises in the README (alt text, event
dates, external links), the page inventory in ``content/navigation.py``, and a
small HTML audit that keeps accessibility regressions (duplicate ids, missing
alt, extra h1) from slipping back in.
"""

import shutil
import tempfile
from datetime import timedelta
from html.parser import HTMLParser
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from PIL import Image

from content import prototype_data
from content.event_images import event_image
from content.models import (
    Agency,
    Article,
    Complaint,
    ComplaintUpdate,
    ContactMessage,
    Document,
    Event,
    Feedback,
    Notice,
    Office,
    Service,
    validate_image_size,
)
from content.navigation import MAIN_NAV, PAGES


class HtmlAudit(HTMLParser):
    """Collect the handful of things we assert on in rendered pages."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.ids = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "img":
            self.images.append(attrs)


def audit(response):
    parser = HtmlAudit()
    parser.feed(response.content.decode("utf-8"))
    return parser


class AltTextRuleTests(TestCase):
    def make_article(self, **overrides):
        data = {
            "title": "Test article",
            "slug": "test-article",
            "summary": "One sentence.",
            "body": "Body copy.",
        }
        data.update(overrides)
        return Article(**data)

    def test_image_requires_alt_text(self):
        article = self.make_article(
            image=SimpleUploadedFile("photo.png", b"fake", content_type="image/png")
        )
        with self.assertRaises(ValidationError) as caught:
            article.full_clean()
        self.assertIn("image_alt", caught.exception.message_dict)

    def test_no_image_means_alt_can_stay_blank(self):
        self.make_article().full_clean()

    def test_oversized_image_is_rejected(self):
        big = SimpleUploadedFile("big.png", b"x" * (2 * 1024 * 1024 + 1), content_type="image/png")
        with self.assertRaises(ValidationError):
            validate_image_size(big)

    def test_notice_image_also_requires_alt_text(self):
        notice = Notice(
            title="Advisory",
            slug="advisory",
            body="Details.",
            image=SimpleUploadedFile("notice.png", b"fake", content_type="image/png"),
        )
        with self.assertRaises(ValidationError) as caught:
            notice.full_clean()
        self.assertIn("image_alt", caught.exception.message_dict)


class EventRuleTests(TestCase):
    def make_event(self, **overrides):
        start = timezone.now()
        data = {
            "title": "Test event",
            "slug": "test-event",
            "description": "Details.",
            "start_datetime": start,
            "end_datetime": start + timedelta(hours=2),
            "venue": "City Hall",
        }
        data.update(overrides)
        return Event(**data)

    def test_end_before_start_is_rejected(self):
        start = timezone.now()
        event = self.make_event(start_datetime=start, end_datetime=start - timedelta(hours=1))
        with self.assertRaises(ValidationError) as caught:
            event.full_clean()
        self.assertIn("end_datetime", caught.exception.message_dict)

    def test_open_ended_event_is_allowed(self):
        self.make_event(end_datetime=None).full_clean()


class ServiceLinkRuleTests(TestCase):
    def test_external_link_must_be_https(self):
        service = Service(
            name="Portal",
            description="Outside service.",
            url="http://example.com",
            is_external=True,
        )
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_internal_link_must_start_with_slash(self):
        service = Service(
            name="Permits",
            description="Permit page.",
            url="permits/",
            is_external=False,
        )
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_staging_urls_are_rejected(self):
        service = Service(
            name="Permits",
            description="Permit page.",
            url="/tempmain/permits/",
            is_external=False,
        )
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_valid_links_pass(self):
        Service(
            name="Permits",
            description="Permit page.",
            url="/government/",
            is_external=False,
        ).full_clean()
        Service(
            name="eFOI",
            description="National portal.",
            url="https://www.foi.gov.ph/",
            is_external=True,
        ).full_clean()


class NavigationTests(TestCase):
    def test_page_names_and_routes_are_unique(self):
        names = [name for name, _route, _title in PAGES]
        routes = [route for _name, route, _title in PAGES]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(routes), len(set(routes)))

    def test_every_main_nav_item_has_a_page(self):
        # Home is a real view on the "" route rather than a PAGES
        # placeholder, so the contract is that every nav item reverses to a
        # working URL (reverse() raises NoReverseMatch when it does not).
        for name, _label in MAIN_NAV:
            with self.subTest(item=name):
                self.assertTrue(reverse(name).startswith("/"))

    def test_every_page_url_reverses(self):
        for name, _route, _title in PAGES:
            self.assertTrue(reverse(name).startswith("/"))


class PageRenderingTests(TestCase):
    def test_every_page_returns_ok(self):
        for name, _route, _title in PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_every_page_has_one_h1_and_unique_ids(self):
        for name, _route, _title in PAGES:
            with self.subTest(page=name):
                result = audit(self.client.get(reverse(name)))
                self.assertEqual(result.h1_count, 1)
                duplicates = {i for i in result.ids if result.ids.count(i) > 1}
                self.assertEqual(duplicates, set(), f"duplicate ids: {duplicates}")

    def test_every_image_has_an_alt_attribute(self):
        for name, _route, _title in PAGES:
            with self.subTest(page=name):
                result = audit(self.client.get(reverse(name)))
                for image in result.images:
                    self.assertIn("alt", image, f"missing alt on {image.get('src')}")

    def test_accessibility_page_shows_the_commitment_text(self):
        response = self.client.get(reverse("accessibility"))
        self.assertContains(response, "Magna Carta")
        self.assertContains(response, "WCAG 2.2")
        self.assertNotContains(response, "WCAG 2.1")

    def test_sitemap_lists_every_page(self):
        response = self.client.get(reverse("sitemap_page"))
        for name, _route, title in PAGES:
            with self.subTest(page=name):
                # Titles are HTML-escaped by the template ("News &amp; updates").
                self.assertContains(response, escape(title))

    def test_current_page_is_marked_in_the_main_nav(self):
        response = self.client.get(reverse("about"))
        current = [item for item in response.context["NAV_ITEMS"] if item["is_current"]]
        self.assertEqual([item["url"] for item in current], [reverse("about")])


class NewsTests(TestCase):
    def test_every_article_opens(self):
        for article in prototype_data.NEWS_ARTICLES:
            with self.subTest(slug=article["slug"]):
                response = self.client.get(reverse("news_detail", args=[article["slug"]]))
                self.assertEqual(response.status_code, 200)

    def test_unknown_article_returns_404(self):
        response = self.client.get(reverse("news_detail", args=["not-a-real-slug"]))
        self.assertEqual(response.status_code, 404)


class DatabaseContentTests(TestCase):
    """Public pages prefer published database content over prototype copy."""

    def make_article(self, **overrides):
        data = {
            "title": "City opens new satellite office",
            "slug": "city-opens-new-satellite-office",
            "summary": "Residents can process permits closer to home.",
            "body": "The new desk opens on Monday.",
        }
        data.update(overrides)
        return Article.objects.create(**data)

    def test_home_and_news_prefer_database_articles(self):
        article = self.make_article()
        for name in ("home", "news"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertContains(response, article.title)
                self.assertNotContains(response, prototype_data.NEWS_ARTICLES[0]["title"])

    def test_future_dated_article_is_hidden_from_listings_and_detail(self):
        hidden = self.make_article(
            title="Embargoed story",
            slug="embargoed-story",
            published_at=timezone.now() + timedelta(days=2),
        )
        for name in ("home", "news"):
            with self.subTest(page=name):
                self.assertNotContains(self.client.get(reverse(name)), hidden.title)
        self.assertEqual(
            self.client.get(reverse("news_detail", args=[hidden.slug])).status_code,
            404,
        )

    def test_published_article_detail_renders(self):
        article = self.make_article()
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)
        self.assertContains(response, article.body)

    def test_public_notice_detail_and_future_notice(self):
        notice = Notice.objects.create(
            title="Water service interruption",
            slug="water-service-interruption",
            body="Work runs from 9:00 AM to 3:00 PM.",
        )
        future = Notice.objects.create(
            title="Scheduled for later",
            slug="scheduled-for-later",
            body="Not yet public.",
            published_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(notice.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, notice.title)
        self.assertEqual(
            self.client.get(future.get_absolute_url()).status_code,
            404,
        )

    def test_event_detail_renders(self):
        event = Event.objects.create(
            title="Barangay clean-up day",
            slug="barangay-clean-up-day",
            description="Join the city-wide coastal clean-up.",
            start_datetime=timezone.now() + timedelta(days=3),
            venue="Pristine Beach",
        )
        response = self.client.get(event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, event.title)
        self.assertContains(response, "Pristine Beach")


class EventImageTests(TestCase):
    """Event pages use an uploaded photo, then a local official fallback."""

    def make_event(self, **overrides):
        data = {
            "title": "Coastal clean-up",
            "slug": "coastal-clean-up",
            "description": "Join the city-wide clean-up.",
            "start_datetime": timezone.now() + timedelta(days=2),
            "venue": "Pristine Beach",
        }
        data.update(overrides)
        return Event.objects.create(**data)

    def test_official_event_photo_is_used_as_a_fallback(self):
        event = self.make_event(
            title="Fun Fishing Day at Balayong People's Park",
            slug="fun-fishing-day-at-balayong-peoples-park",
        )
        self.assertContains(self.client.get(event.get_absolute_url()), "img/banner/fun-fishing-day")
        self.assertEqual(
            event_image(event)["url"],
            f"{settings.STATIC_URL}img/banner/fun-fishing-day.jpg",
        )

    def test_uploaded_image_wins_over_the_fallback(self):
        event = self.make_event(slug="fun-fishing-day-at-balayong-peoples-park")
        event.image = SimpleUploadedFile("own-photo.png", b"fake", content_type="image/png")
        event.image.name = "images/own-photo.png"
        event.image_alt = "Staff photo from the event."
        image = event_image(event)
        self.assertEqual(image["alt"], "Staff photo from the event.")
        self.assertIn("own-photo", image["url"])
        self.assertNotIn("img/banner/fun-fishing-day", image["url"])


class SearchTests(TestCase):
    def test_empty_search_page_loads(self):
        self.assertEqual(self.client.get(reverse("search")).status_code, 200)

    def test_query_is_echoed_and_escaped(self):
        response = self.client.get(reverse("search"), {"q": "<script>alert(1)</script>"})
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")


class ContactFormTests(TestCase):
    def test_post_without_javascript_saves_and_redirects(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Maria Santos",
                "email": "maria@example.com",
                "phone": "09171234567",
                "topic": "General inquiry",
                "message": "Hello, I have a question about office hours.",
                "consent": "on",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Maria Santos")
        self.assertEqual(message.topic, "General inquiry")
        self.assertTrue(message.consent)

    def test_missing_consent_blocks_submission(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Maria Santos",
                "email": "maria@example.com",
                "message": "Hello",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "Please agree to the privacy notice")


class PrivacyTests(TestCase):
    def test_map_is_not_embedded_until_the_visitor_asks(self):
        response = self.client.get(reverse("contact"))
        # The HTML must not contain the Google iframe: a page view alone must
        # not send the visitor's IP address to a third party.
        self.assertNotContains(response, "<iframe")
        self.assertContains(response, "data-map-load")
        self.assertContains(response, "Load the map")

    def test_contact_form_explains_use_retention_and_the_dpo(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "How we use your message")
        self.assertContains(response, "two years")
        self.assertContains(response, "Data Protection Officer")
        self.assertContains(response, "withdraw consent")

    def test_privacy_policy_covers_retention_third_parties_and_complaints(self):
        response = self.client.get(reverse("privacy"))
        for anchor in (
            "collect",
            "use",
            "retention",
            "third-parties",
            "cookies",
            "security",
            "rights",
            "dpo",
        ):
            with self.subTest(anchor=anchor):
                self.assertContains(response, f'id="{anchor}"')
        self.assertContains(response, "two years")
        self.assertContains(response, "30 days")
        self.assertContains(response, "National Privacy Commission")
        self.assertContains(response, "Google")


class ErrorPageTests(TestCase):
    @override_settings(DEBUG=False)
    def test_unknown_url_uses_the_branded_404_page(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "We can't find that page", status_code=404)
        self.assertContains(response, reverse("directory"), status_code=404)

    def test_500_page_renders_without_request_context(self):
        # The default 500 handler renders with an empty context: the template
        # must not depend on context processors or database state.
        html = render_to_string("500.html")
        self.assertIn("Something went wrong", html)
        self.assertNotIn("{{", html)


class CrawlerFileTests(TestCase):
    def test_robots_txt_points_at_the_sitemap(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        self.assertContains(response, f"Sitemap: {settings.SITE_URL}/sitemap.xml")
        self.assertContains(response, "Disallow: /admin/")

    def test_sitemap_xml_lists_pages_and_published_articles(self):
        article = Article.objects.create(
            title="City opens new satellite office",
            slug="city-opens-satellite-office",
            summary="A second service desk opens in the north.",
            body="Residents can now process permits closer to home.",
        )
        hidden = Article.objects.create(
            title="Embargoed until next month",
            slug="embargoed-until-next-month",
            summary="This article should stay out of the sitemap.",
            body="Not yet public.",
            published_at=timezone.now() + timedelta(days=30),
        )
        response = self.client.get(reverse("sitemap_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        self.assertContains(response, reverse("home"))
        for name, _route, _title in PAGES:
            if name != "sitemap_page":
                with self.subTest(page=name):
                    self.assertContains(response, reverse(name))
        self.assertContains(response, article.get_absolute_url())
        self.assertNotContains(response, hidden.get_absolute_url())

    def test_sitemap_xml_skips_the_html_site_map(self):
        response = self.client.get(reverse("sitemap_xml"))
        self.assertNotContains(response, reverse("sitemap_page"))

    def test_sitemap_lists_only_documents_hosted_here(self):
        external = Document.objects.create(
            title="National budget portal",
            slug="national-budget-portal",
            external_url="https://example.gov.ph/budget/",
        )
        response = self.client.get(reverse("sitemap_xml"))
        self.assertNotContains(response, external.external_url)
        self.assertNotContains(response, "testserverhttps")


class SumbunganTests(TestCase):
    def setUp(self):
        self.agency = Agency.objects.create(
            name="City Engineer's Office",
            slug="city-engineers-office",
            category=Agency.Category.INFRASTRUCTURE,
        )

    def payload(self, **overrides):
        data = {
            "category": Complaint.Category.INFRASTRUCTURE,
            "subject": "Broken street light on Rizal Avenue",
            "barangay": "San Pedro",
            "landmark": "Near the plaza",
            "details": "The light near the plaza is out every night.",
            "name": "Maria Santos",
            "email": "maria@example.com",
            "phone": "",
            "consent": "on",
        }
        data.update(overrides)
        return data

    def test_form_page_loads(self):
        self.assertEqual(self.client.get(reverse("sumbungan")).status_code, 200)

    def test_valid_submission_creates_reference_and_first_update(self):
        response = self.client.post(reverse("sumbungan"), self.payload())
        complaint = Complaint.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], complaint.get_absolute_url())
        self.assertRegex(complaint.reference, r"^PPC-\d{4}-\d{6}$")
        self.assertEqual(complaint.agency, self.agency)
        self.assertEqual(complaint.updates.count(), 1)
        self.assertEqual(complaint.updates.first().status, Complaint.Status.RECEIVED)

    def test_anonymous_submission_clears_contact_details(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(
                is_anonymous="on",
                name="",
                email="",
                phone="",
            ),
        )
        self.assertEqual(response.status_code, 302)
        complaint = Complaint.objects.get()
        self.assertTrue(complaint.is_anonymous)
        self.assertEqual(complaint.name, "")
        self.assertEqual(complaint.email, "")
        self.assertEqual(complaint.phone, "")

    def test_named_submission_needs_a_contact_detail(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(email="", phone=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add an email or mobile number")
        self.assertFalse(Complaint.objects.exists())

    def test_consent_is_required(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(consent=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please agree to the privacy notice")
        self.assertFalse(Complaint.objects.exists())

    def test_barangay_is_required(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(barangay=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertFalse(Complaint.objects.exists())

    def test_honeypot_submission_is_rejected(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(website="https://spam.example"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Something went wrong")
        self.assertFalse(Complaint.objects.exists())

    def test_internal_updates_stay_off_the_public_tracking_page(self):
        self.client.post(reverse("sumbungan"), self.payload())
        complaint = Complaint.objects.get()
        ComplaintUpdate.objects.create(
            complaint=complaint,
            status=Complaint.Status.IN_REVIEW,
            note="Resident called; verified the address.",
        )
        ComplaintUpdate.objects.create(
            complaint=complaint,
            status=Complaint.Status.IN_REVIEW,
            note="Internal-only triage note.",
            is_public=False,
        )
        response = self.client.get(complaint.get_absolute_url())
        self.assertContains(response, "Resident called; verified the address.")
        self.assertNotContains(response, "Internal-only triage note.")

    def test_tracking_page_shows_barangay_and_sla_due_date(self):
        self.client.post(reverse("sumbungan"), self.payload())
        complaint = Complaint.objects.get()
        response = self.client.get(complaint.get_absolute_url())
        self.assertContains(response, complaint.barangay)
        self.assertContains(response, "Near the plaza")
        self.assertContains(response, f"{complaint.due_at:%B} {complaint.due_at.day}")

    def test_complaint_is_overdue_after_its_sla_window(self):
        complaint = Complaint.objects.create(
            category=Complaint.Category.INFRASTRUCTURE,
            subject="Old pothole",
            details="Still there.",
            is_anonymous=True,
            consent=True,
        )
        Complaint.objects.filter(pk=complaint.pk).update(
            created_at=timezone.now() - timedelta(days=complaint.sla_days + 1)
        )
        complaint.refresh_from_db()
        self.assertTrue(complaint.is_overdue)

        complaint.status = Complaint.Status.RESOLVED
        self.assertFalse(complaint.is_overdue)

    def test_tracking_page_hides_contact_details(self):
        self.client.post(reverse("sumbungan"), self.payload())
        complaint = Complaint.objects.get()
        response = self.client.get(complaint.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, complaint.subject)
        self.assertNotContains(response, "maria@example.com")
        self.assertNotContains(response, "Maria Santos")

    def test_tracking_lookup_redirects_on_a_known_reference(self):
        self.client.post(reverse("sumbungan"), self.payload())
        complaint = Complaint.objects.get()
        response = self.client.post(
            reverse("complaint_track"), {"reference": complaint.reference.lower()}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], complaint.get_absolute_url())

    def test_unknown_reference_shows_a_helpful_error(self):
        response = self.client.post(reverse("complaint_track"), {"reference": "PPC-2026-999999"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "could not find that reference")


class PhotoUploadTests(TestCase):
    """Photo handling keeps storage small and location data private."""

    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)
        self.override = override_settings(MEDIA_ROOT=self.media_root)
        self.override.enable()
        self.addCleanup(self.override.disable)

    def payload(self, **overrides):
        data = {
            "category": Complaint.Category.SANITATION,
            "subject": "Uncollected garbage",
            "barangay": "San Pedro",
            "details": "The bin on the corner has not been collected this week.",
            "name": "Maria Santos",
            "email": "maria@example.com",
            "consent": "on",
        }
        data.update(overrides)
        return data

    def photo(self, name="street.jpg", fmt="JPEG"):
        buffer = BytesIO()
        image = Image.new("RGB", (48, 32), (30, 120, 200))
        exif = Image.Exif()
        exif[0x010F] = "SecretCameraMake"
        image.save(buffer, format=fmt, exif=exif.tobytes())
        return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")

    def test_photo_is_reencoded_as_webp_and_strips_metadata(self):
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(attachments=[self.photo()]),
        )
        self.assertEqual(response.status_code, 302)
        complaint = Complaint.objects.get()
        attachment = complaint.attachments.get()
        self.assertTrue(attachment.file.name.endswith(".webp"))
        self.assertEqual(attachment.content_type, "image/webp")
        self.assertEqual(attachment.original_name, "street.jpg")

        attachment.file.open("rb")
        try:
            data = attachment.file.read()
        finally:
            attachment.file.close()
        self.assertNotIn(b"SecretCameraMake", data)
        self.assertEqual(Image.open(BytesIO(data)).format, "WEBP")
        self.assertIn("1 photo(s) attached", complaint.updates.get().note)

    def test_wrong_file_type_is_rejected(self):
        buffer = BytesIO()
        Image.new("RGB", (16, 16)).save(buffer, format="GIF")
        upload = SimpleUploadedFile("map.gif", buffer.getvalue(), content_type="image/gif")
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(attachments=[upload]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload JPG, PNG, or WebP photos only.")
        self.assertFalse(Complaint.objects.exists())

    def test_oversized_photo_is_rejected(self):
        upload = SimpleUploadedFile(
            "huge.jpg",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="image/jpeg",
        )
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(attachments=[upload]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Each photo must be 5 MB or smaller.")
        self.assertFalse(Complaint.objects.exists())

    def test_more_than_three_photos_is_rejected(self):
        uploads = [self.photo(name=f"photo-{index}.jpg") for index in range(4)]
        response = self.client.post(
            reverse("sumbungan"),
            self.payload(attachments=uploads),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Attach up to 3 photos.")
        self.assertFalse(Complaint.objects.exists())


class FeedbackTests(TestCase):
    def test_normal_post_creates_feedback_and_redirects(self):
        response = self.client.post(
            reverse("submit_feedback"),
            {"page": "/directory/", "helpful": "1", "next": "/directory/"},
        )
        self.assertEqual(response.status_code, 302)
        item = Feedback.objects.get()
        self.assertTrue(item.helpful)
        self.assertEqual(item.page, "/directory/")

    def test_ajax_post_returns_json(self):
        response = self.client.post(
            reverse("submit_feedback"),
            {"page": "/", "helpful": "0", "comment": "Hard to read"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertFalse(Feedback.objects.get().helpful)

    def test_invalid_answer_is_rejected(self):
        response = self.client.post(reverse("submit_feedback"), {"page": "/", "helpful": "maybe"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Feedback.objects.exists())

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get(reverse("submit_feedback")).status_code, 405)

    def test_feedback_widget_appears_on_public_pages(self):
        response = self.client.get(reverse("directory"))
        self.assertContains(response, "Was this page helpful?")


class FaqAssistantTests(TestCase):
    def test_faq_page_lists_questions(self):
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How do I file a complaint or request help?")

    def test_ask_matches_a_keyword_and_returns_a_link(self):
        response = self.client.get(reverse("faq_ask"), {"q": "business permit"})
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertIn("permit", data["answer"].lower())
        self.assertTrue(data["url"])

    def test_ask_falls_back_without_inventing_an_answer(self):
        response = self.client.get(reverse("faq_ask"), {"q": "quantum flux capacitor"})
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertIn("don't have a ready answer", data["answer"])
        self.assertEqual(data["url"], reverse("faq"))


class DirectoryTests(TestCase):
    def setUp(self):
        self.agency = Agency.objects.create(
            name="City Treasurer's Office", slug="city-treasurers-office"
        )
        self.office = Office.objects.create(
            name="Business Permits and Licensing Office",
            slug="bplo",
            agency=self.agency,
            description="New and renewing business permits.",
            phone="(048) 000-0000",
            phone_digits="0480000000",
        )

    def test_directory_uses_database_offices(self):
        response = self.client.get(reverse("directory"))
        self.assertContains(response, self.office.name)
        self.assertContains(response, "City Treasurer&#x27;s Office")

    def test_search_filters_offices(self):
        response = self.client.get(reverse("directory"), {"q": "licensing"})
        self.assertContains(response, self.office.name)
        response = self.client.get(reverse("directory"), {"q": "nothing-matches"})
        self.assertContains(response, "No office matches that search")

    def test_agency_filter(self):
        other = Agency.objects.create(name="City Health Office", slug="cho")
        Office.objects.create(name="Health Centre", slug="health-centre", agency=other)
        response = self.client.get(reverse("directory"), {"agency": self.agency.pk})
        self.assertContains(response, self.office.name)
        self.assertNotContains(response, "Health Centre")


class MultimodalSearchTests(TestCase):
    def setUp(self):
        Service.objects.create(
            name="Business Permit Renewal",
            description="Renew a mayor's permit online.",
            url="/government/",
        )
        Office.objects.create(
            name="Business Permits and Licensing Office",
            slug="bplo",
            description="Permits desk.",
        )

    def test_search_finds_database_services(self):
        response = self.client.get(reverse("search"), {"q": "permit"})
        self.assertContains(response, "Business Permit Renewal")
        self.assertContains(response, "Business Permits and Licensing Office")

    def test_type_filter_narrows_results(self):
        response = self.client.get(reverse("search"), {"q": "permit", "type": "Service"})
        self.assertContains(response, "Business Permit Renewal")
        self.assertNotContains(response, "Business Permits and Licensing Office")
        self.assertEqual(response.context["kind"], "Service")

    def test_no_results_page_offers_next_steps(self):
        response = self.client.get(reverse("search"), {"q": "zzzzzz-no-match"})
        self.assertContains(response, "No results for")
        self.assertContains(response, reverse("faq"))
