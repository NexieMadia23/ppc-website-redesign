"""Tests for the news data layer: what the public site may show, and how it pages.

The seed command is deliberately NOT run here: every test builds its own rows, so
these tests stay correct once the curated content is replaced by real entries.
"""

import re
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Event, Notice, Service
from .navigation import MAIN_NAV, PAGES


def make_article(**overrides):
    defaults = {
        "title": "Test headline",
        "slug": "test-headline",
        "summary": "A short summary.",
        "body": "First paragraph.\n\nSecond paragraph.",
        "author": "City Information Office",
        "category": Article.Category.CITY_GOVERNMENT,
    }
    defaults.update(overrides)
    return Article.objects.create(**defaults)


def make_event(**overrides):
    defaults = {
        "title": "Test event",
        "slug": "test-event",
        "start_datetime": timezone.now() + timedelta(days=3),
        "venue": "City Baywalk",
    }
    defaults.update(overrides)
    return Event.objects.create(**defaults)


class ArticleModelTests(TestCase):
    def test_paragraphs_split_on_blank_lines(self):
        article = make_article()
        self.assertEqual(article.paragraphs, ["First paragraph.", "Second paragraph."])

    def test_date_is_the_published_day(self):
        article = make_article()
        self.assertEqual(article.date, article.published_at.date())


class ArticleVisibilityTests(TestCase):
    def test_future_article_is_hidden_from_the_listing(self):
        make_article(slug="upcoming", published_at=timezone.now() + timedelta(days=2))
        response = self.client.get(reverse("news"))
        self.assertNotContains(response, "Test headline")

    def test_future_article_returns_404_on_its_own_url(self):
        make_article(slug="upcoming", published_at=timezone.now() + timedelta(days=2))
        response = self.client.get(reverse("news_detail", args=["upcoming"]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_slug_returns_404(self):
        response = self.client.get(reverse("news_detail", args=["does-not-exist"]))
        self.assertEqual(response.status_code, 404)

    def test_published_article_shows_its_byline_and_paragraphs(self):
        make_article(slug="published-story", author="Charlito Christopher Padul, CIO")
        response = self.client.get(reverse("news_detail", args=["published-story"]))
        self.assertContains(response, "Charlito Christopher Padul, CIO")
        self.assertContains(response, "First paragraph.")
        self.assertContains(response, "Second paragraph.")


class NewsListingTests(TestCase):
    def test_articles_are_paged(self):
        for index in range(5):
            make_article(slug=f"story-{index}", title=f"Story {index}")
        with self.settings(NEWS_PER_PAGE=2):
            first = self.client.get(reverse("news"))
        self.assertEqual(len(first.context["articles"]), 2)
        self.assertEqual(first.context["paginator"].num_pages, 3)
        self.assertContains(first, "Older stories")

    def test_page_beyond_the_end_clamps_to_the_last_page(self):
        for index in range(5):
            make_article(slug=f"story-{index}", title=f"Story {index}")
        with self.settings(NEWS_PER_PAGE=2):
            response = self.client.get(reverse("news"), {"page": "999"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 3)

    def test_category_filter_returns_only_that_section(self):
        make_article(slug="council-story", category=Article.Category.CITY_COUNCIL)
        make_article(slug="health-story", category=Article.Category.HEALTH)
        response = self.client.get(reverse("news"), {"category": "health"})
        self.assertContains(response, "health-story")
        self.assertNotContains(response, "council-story")

    def test_unknown_category_shows_everything(self):
        make_article(slug="council-story", category=Article.Category.CITY_COUNCIL)
        response = self.client.get(reverse("news"), {"category": "not-a-section"})
        self.assertContains(response, "council-story")
        self.assertEqual(response.context["active_category"], "")

    def test_filter_bar_offers_only_sections_that_have_articles(self):
        make_article(slug="council-story", category=Article.Category.CITY_COUNCIL)
        response = self.client.get(reverse("news"))
        offered = [value for value, _label in response.context["categories"]]
        self.assertEqual(offered, ["city-council"])


class HomepageTests(TestCase):
    def test_home_shows_the_three_latest_articles(self):
        for index in range(4):
            make_article(
                slug=f"story-{index}",
                title=f"Story {index}",
                published_at=timezone.now() - timedelta(days=index),
            )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Story 0")
        self.assertContains(response, "Story 2")
        self.assertNotContains(response, "Story 3")

    def test_home_shows_only_events_that_have_not_started(self):
        make_event(
            slug="past-event", title="Fun Fishing Day (last month)",
            start_datetime=timezone.now() - timedelta(days=1),
        )
        make_event(
            slug="future-event", title="Fun Fishing Day",
            start_datetime=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Fun Fishing Day")
        self.assertNotContains(response, "last month")

    def test_urgent_notice_is_the_advisory_and_is_not_listed_twice(self):
        urgent = Notice.objects.create(
            title="Water interruption", slug="water-interruption",
            body="Store water in advance.", is_urgent=True,
        )
        Notice.objects.create(title="Clinic hours", slug="clinic-hours")
        response = self.client.get(reverse("home"))
        self.assertContains(response, urgent.title)
        self.assertEqual(response.context["urgent_notice"], urgent)
        # The advisory banner renders it once; the notice list must skip it.
        self.assertEqual(response.content.decode().count("Water interruption"), 1)

    def test_services_are_split_into_portals_and_offices(self):
        Service.objects.create(
            name="e-Payment", description="Pay online.", url="https://example.com/pay",
            is_external=True, section=Service.Section.PORTALS,
        )
        Service.objects.create(
            name="City Tourism", description="Plan a trip.", url="https://example.com/tourism",
            is_external=True, section=Service.Section.OFFICES,
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["eportals"]), 1)
        self.assertEqual(len(response.context["services"]), 1)


class LinkIntegrityTests(TestCase):
    """The live site ships empty hrefs and staging links; the redesign must not."""

    def test_listing_pages_render_without_an_empty_href(self):
        make_article(slug="story")
        Notice.objects.create(title="Clinic hours", slug="clinic-hours")
        make_event(slug="future-event")
        for url in (reverse("home"), reverse("news")):
            html = self.client.get(url).content.decode()
            self.assertNotIn('href=""', html, f"empty href on {url}")
            self.assertNotIn("tempmain", html, f"staging link on {url}")

    def test_a_notice_without_a_url_renders_plain_text(self):
        Notice.objects.create(title="Clinic hours", slug="clinic-hours")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Clinic hours")
        self.assertContains(response, "notice-list__plain")


class ServiceValidationTests(TestCase):
    def test_staging_urls_are_rejected(self):
        service = Service(name="Broken", description="x", url="https://tempmain.example.com/x")
        with self.assertRaisesMessage(Exception, "Staging URLs are not allowed."):
            service.full_clean()

    def test_events_reject_internal_looking_external_urls(self):
        event = make_event(slug="event")
        event.url = "example.com"
        with self.assertRaisesMessage(Exception, "Use '/' for an internal page"):
            event.full_clean()


class SiteIntegrityTests(TestCase):
    """The defects found on the live site, encoded as tests.

    The public site shipped empty hrefs, staging URLs, dead tel:/mailto: links, a
    link to the wrong agency, duplicated section ids, and markup leaking into
    visible text. Every page must stay clean of all of them.
    """

    # Tokens that only ever appear in a link when internal infrastructure has
    # leaked into public markup.
    LEAKY_TOKENS = (
        "tempmain", "localhost", "127.0.0.1", "0.0.0.0", ":8000", ":8080",
        "staging", ".test/", ".local/", "ngrok", "herokuapp", "file://",
    )

    # Pseudo-bold and fullwidth characters look bold but are read letter by
    # letter by screen readers, so they must never reach published copy.
    def suspicious_characters(self, html):
        return [
            ch for ch in html
            if 0x1D400 <= ord(ch) <= 0x1D7FF
            or 0xFF00 <= ord(ch) <= 0xFFEF
            or 0x202A <= ord(ch) <= 0x202E
            or ord(ch) == 0xFEFF
        ]

    def paths(self):
        return [reverse("home")] + [reverse(name) for name, _path, _title in PAGES]

    def test_no_page_ships_an_empty_or_external_wrong_link(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            self.assertNotIn('href=""', html, f"empty href on {url}")
            self.assertNotIn("dole.gov.ph", html.lower(), f"wrong-agency link on {url}")
            for token in self.LEAKY_TOKENS:
                self.assertNotIn(token, html, f"{url} exposes {token!r}")

    def test_no_page_leaks_template_syntax_or_unicode_tricks(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            for token in ("{{", "}}", "{%", "%}"):
                self.assertNotIn(token, html, f"{url} shows unrendered {token!r}")
            leaked = self.suspicious_characters(html)
            self.assertEqual(leaked, [], f"{url} contains {leaked}")

    def test_phone_and_email_links_are_well_formed(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            for href in re.findall(r'href="(tel:[^"]*)"', html):
                self.assertRegex(href, r"^tel:\+?\d{3,}$", f"{url}: {href}")
            for href in re.findall(r'href="(mailto:[^"]*)"', html):
                address = href[len("mailto:"):]
                self.assertIn("@", address, f"{url}: {href}")
                self.assertNotIn(" ", address, f"{url}: {href}")

    def test_no_page_repeats_an_id(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            ids = [i for i in re.findall(r'\sid="([^"]+)"', html) if not i.startswith("icon-")]
            repeated = sorted({i for i in ids if ids.count(i) > 1})
            self.assertEqual(repeated, [], f"{url} repeats ids: {repeated}")

    def test_no_page_leaks_markup_into_visible_text(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            leaked = re.search(r"&lt;(p|div|span|br|strong|a)\b", html)
            self.assertIsNone(leaked, f"leaked markup on {url}")

    def test_accessibility_statement_keeps_its_commitment_section(self):
        html = self.client.get(reverse("accessibility")).content.decode()
        self.assertIn("WCAG", html)
        self.assertEqual(html.count('id="limitations"'), 1)

    def test_every_page_anchor_has_exactly_one_target(self):
        for url in self.paths():
            html = self.client.get(url).content.decode()
            anchors = set(re.findall(r'href="#([^"]+)"', html))
            for anchor in anchors:
                count = html.count(f'id="{anchor}"')
                self.assertEqual(count, 1, f"{url}: #{anchor} matches {count} elements")

    def test_every_page_has_one_h1_and_no_skipped_heading_level(self):
        """Text hierarchy: one H1, and never a jump like H1 straight to H3."""
        for url in self.paths():
            html = self.client.get(url).content.decode()
            levels = [int(m) for m in re.findall(r"<h([1-6])[^>]*>", html)]
            self.assertEqual(levels.count(1), 1, f"{url}: expected exactly one H1")
            self.assertEqual(levels[0], 1, f"{url}: the first heading must be the H1")
            previous = 0
            for level in levels:
                self.assertLessEqual(
                    level, previous + 1,
                    f"{url}: heading level jumps from H{previous} to H{level}",
                )
                previous = level

    def test_document_title_matches_the_page_h1(self):
        """A page's <title> and its H1 name the same page, word for word."""
        for url in self.paths():
            html = self.client.get(url).content.decode()
            title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
            title = title.split(" | ")[0].split(" — ")[0].strip()
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
            h1 = re.sub(r"<[^>]+>", "", h1).strip()
            self.assertEqual(title, h1, f"{url}: title {title!r} != H1 {h1!r}")

    def test_menu_label_matches_the_page_title(self):
        """The menu name and the page title are the same words (no drift)."""
        titles = {name: title for name, _path, title in PAGES}
        for name, label in MAIN_NAV:
            self.assertEqual(label, titles[name], f"{name}: menu {label!r} != page {titles[name]!r}")

    def test_new_tab_claims_are_true(self):
        """Nothing may claim 'opens in a new tab' unless the link really does."""
        for url in self.paths():
            html = self.client.get(url).content.decode()
            self.assertNotIn("opens in a new tab", html, f"{url} claims a new tab")
            self.assertNotIn('target="_blank"', html, f"{url} opens a new tab")

