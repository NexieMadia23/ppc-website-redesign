"""Tests for the news data layer: what the public site may show, and how it pages.

The seed command is deliberately NOT run here: every test builds its own rows, so
these tests stay correct once the curated content is replaced by real entries.
"""

import re
from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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


def make_emergency_contact(**overrides):
    defaults = {
        "name": "Test Hotline",
        "number": "(048) 000-0000",
        "digits": "+63480000000",
        "note": "For tests.",
    }
    defaults.update(overrides)
    return EmergencyContact.objects.create(**defaults)


def make_office(**overrides):
    defaults = {
        "name": "Test Office",
        "phone": "(048) 111-1111",
        "digits": "+63481111111",
        "note": "Handles tests.",
    }
    defaults.update(overrides)
    return DirectoryOffice.objects.create(**defaults)


def make_contact_details(**overrides):
    defaults = {
        "address": "City Hall, Rizal Avenue",
        "phone": "(048) 717-8000",
        "phone_digits": "+63487178000",
        "email": "info@puertoprincesa.ph",
        "hours": "Mondays to Fridays",
        "facebook": "https://www.facebook.com/puertoprincesaph",
        "map_url": "https://maps.app.goo.gl/example",
        "map_embed": "https://maps.google.com/maps?q=x&output=embed",
    }
    defaults.update(overrides)
    details = ContactDetails(pk=1, **defaults)
    details.save()
    return details


class DirectoryAndEmergencyTests(TestCase):
    """Phase 2: the directory, the emergency page and the quick-dial sheet read
    the database instead of content/prototype_data.py."""

    def test_directory_lists_offices_from_the_database(self):
        make_office(name="City Agriculture Office", phone="(048) 222-2222", digits="+63482222222")
        response = self.client.get(reverse("directory"))
        self.assertContains(response, "City Agriculture Office")
        self.assertContains(response, "tel:+63482222222")
        self.assertNotContains(response, "Prototype preview")

    def test_emergency_page_lists_contacts_and_safety_tips(self):
        make_emergency_contact(name="Coast Guard Station")
        SafetyTip.objects.create(title="Before a storm", body="Charge your phone.", order=1)
        response = self.client.get(reverse("emergency"))
        self.assertContains(response, "Coast Guard Station")
        self.assertContains(response, "Before a storm")
        self.assertNotContains(response, "Prototype preview")

    def test_quick_dial_sheet_reads_the_database_on_every_page(self):
        make_emergency_contact(name="Unique Responder Line", number="1234", digits="1234")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Unique Responder Line")

    def test_emergency_contacts_are_ordered_by_the_order_field(self):
        make_emergency_contact(name="Second", order=20)
        make_emergency_contact(name="First", order=10)
        names = list(EmergencyContact.objects.values_list("name", flat=True))
        self.assertEqual(names[0], "First")

    def test_a_contact_cannot_save_digits_with_spaces(self):
        contact = EmergencyContact(name="Bad", number="(048) 000", digits="+6348 000")
        with self.assertRaisesMessage(Exception, "Digits only"):
            contact.full_clean()

    def test_an_office_with_a_phone_must_also_have_digits(self):
        office = DirectoryOffice(name="Bad", phone="(048) 000-0000", digits="")
        with self.assertRaisesMessage(Exception, "Add the digits"):
            office.full_clean()


class ContactPageTests(TestCase):
    """Phase 2: the contact page and the shared contact card read the database."""

    def test_contact_page_shows_details_topics_and_faqs(self):
        make_contact_details(address="1 Test Avenue")
        ContactTopic.objects.create(name="Test topic", order=1)
        ContactFaq.objects.create(question="Test question?", answer="Test answer.", order=1)
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "1 Test Avenue")
        self.assertContains(response, "Test topic")
        self.assertContains(response, "Test question?")
        self.assertNotContains(response, "Prototype preview")

    def test_contact_details_keep_a_single_row(self):
        make_contact_details(address="First address")
        make_contact_details(address="Second address")
        self.assertEqual(ContactDetails.objects.count(), 1)
        self.assertEqual(ContactDetails.load().address, "Second address")

    def test_load_falls_back_to_defaults_when_the_row_is_missing(self):
        details = ContactDetails.load()
        self.assertFalse(details.pk)
        # A tel: link may carry an optional leading + but must be digits only.
        self.assertRegex(details.phone_digits, r"^\+?\d{3,}$")

    def test_contact_details_reject_digits_with_spaces(self):
        details = ContactDetails(
            address="x",
            phone="x",
            phone_digits="+63 48 717 8000",
            email="x@example.com",
            hours="x",
            facebook="https://example.com",
            map_url="https://example.com",
            map_embed="https://example.com",
        )
        with self.assertRaisesMessage(Exception, "Digits only"):
            details.full_clean()


class FloatingNavTests(TestCase):
    """The in-page floating navigation (bottom pill on phones, rail on wider
    screens) must stay a single, labelled, reachable landmark."""

    def test_pages_with_sections_render_one_floating_nav(self):
        html = self.client.get(reverse("about")).content.decode()
        self.assertIn('class="floating-nav"', html)
        self.assertIn('aria-label="Page sections"', html)
        # The retired sticky bar and side rail must not come back.
        self.assertNotIn("section-nav", html)
        self.assertNotIn("side-rail", html)

    def test_each_link_has_a_tooltip_and_a_real_target(self):
        html = self.client.get(reverse("about")).content.decode()
        links = re.findall(
            r'<a class="floating-nav__link" href="#([^"]+)" title="([^"]+)"', html
        )
        self.assertTrue(links, "no section links found")
        for anchor, title in links:
            self.assertEqual(html.count(f'id="{anchor}"'), 1, f"#{anchor} has no unique target")
            self.assertTrue(title.strip(), f"#{anchor} has no tooltip text")

    def test_arrow_controls_the_section_list(self):
        html = self.client.get(reverse("about")).content.decode()
        self.assertIn('aria-controls="floating-nav-list"', html)
        self.assertEqual(html.count('id="floating-nav-list"'), 1)

    def test_the_active_link_is_marked_for_assistive_tech(self):
        """Every page keeps exactly one nav link per section, so the scrollspy
        has a single place to hang aria-current."""
        html = self.client.get(reverse("about")).content.decode()
        targets = re.findall(r'class="floating-nav__link" href="#([^"]+)"', html)
        self.assertEqual(len(targets), len(set(targets)), "a section is listed twice")

