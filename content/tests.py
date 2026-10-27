"""Regression tests for the content app.

These cover the rules the project promises in the README (alt text, event
dates, external links), the page inventory in ``content/navigation.py``, and a
small HTML audit that keeps accessibility regressions (duplicate ids, missing
alt, extra h1) from slipping back in.
"""

from datetime import timedelta
from html.parser import HTMLParser

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from content import prototype_data
from content.models import Article, Event, Service, validate_image_size
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
        page_names = {name for name, _route, _title in PAGES}
        for name, _label in MAIN_NAV:
            self.assertIn(name, page_names)

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
        self.assertContains(response, "WCAG")

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


class SearchTests(TestCase):
    def test_empty_search_page_loads(self):
        self.assertEqual(self.client.get(reverse("search")).status_code, 200)

    def test_query_is_echoed_and_escaped(self):
        response = self.client.get(reverse("search"), {"q": "<script>alert(1)</script>"})
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")


class ContactFormTests(TestCase):
    def test_post_without_javascript_does_not_error(self):
        response = self.client.post(
            reverse("contact"),
            {"name": "Maria Santos", "email": "maria@example.com", "message": "Hello"},
        )
        self.assertEqual(response.status_code, 200)


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

    def test_sitemap_xml_lists_pages_and_articles(self):
        response = self.client.get(reverse("sitemap_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        self.assertContains(response, reverse("home"))
        for name, _route, _title in PAGES:
            if name != "sitemap_page":
                with self.subTest(page=name):
                    self.assertContains(response, reverse(name))
        first = prototype_data.NEWS_ARTICLES[0]["slug"]
        self.assertContains(response, reverse("news_detail", args=[first]))

    def test_sitemap_xml_skips_the_html_site_map(self):
        response = self.client.get(reverse("sitemap_xml"))
        self.assertNotContains(response, reverse("sitemap_page"))
