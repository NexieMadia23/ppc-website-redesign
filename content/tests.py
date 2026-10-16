"""Tests for the news data layer: what the public site may show, and how it pages.

The seed command is deliberately NOT run here: every test builds its own rows, so
these tests stay correct once the curated content is replaced by real entries.
"""

import math
import re
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
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
        # Django only strips single-line {# ... #} comments: a multi-line one is
        # rendered verbatim, which is why "{#" and "#}" are checked here too.
        for url in self.paths():
            html = self.client.get(url).content.decode()
            for token in ("{{", "}}", "{%", "%}", "{#", "#}"):
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
    """The in-page navigation is one landmark in two shapes: a round glass menu
    button that rings the page's items around it on phones, and the same nav
    pinned to the right as a glass rail from tablet width up. Both must stay
    labelled, reachable and complete."""

    # Section links per page. The ring also carries the City Hotlines action,
    # which is not a section, so the ring's item count is one more than this.
    SECTIONS = {"home": 7, "about": 4}

    def _nav(self, name="about"):
        """The rendered page and just its <nav>, so nav markup can be checked
        without the rest of the page getting in the way."""
        html = self.client.get(reverse(name)).content.decode()
        match = re.search(r'<nav class="floating-nav".*?</nav>', html, re.S)
        self.assertIsNotNone(match, "no floating nav rendered")
        return html, match.group(0)

    def _header(self, html):
        match = re.search(r'<header class="site-header".*?</header>', html, re.S)
        self.assertIsNotNone(match, "no site header rendered")
        return match.group(0)

    def test_pages_with_sections_render_one_floating_nav(self):
        html, nav = self._nav()
        self.assertEqual(html.count('class="floating-nav"'), 1)
        self.assertIn('aria-label="Page navigation"', nav)
        # The retired sticky bar and side rail must not come back.
        self.assertNotIn("section-nav", html)
        self.assertNotIn("side-rail", html)

    def test_the_header_no_longer_carries_the_city_hotlines_button(self):
        """City Hotlines moved into the menu, so the header keeps only the search
        bar and must not link to #hotlines a second time."""
        html, _ = self._nav()
        header = self._header(html)
        self.assertNotIn("#hotlines", header)
        self.assertNotIn("City hotlines", header)
        self.assertIn("search", header)

    def test_the_menu_carries_the_city_hotlines_action(self):
        """The menu's City Hotlines entry is the page's only hotlines link, and
        it points at a real page rather than an empty href."""
        html, nav = self._nav()
        self.assertIn('class="floating-nav__link floating-nav__link--action"', nav)
        self.assertIn(f'href="{reverse("directory")}#hotlines"', nav)
        self.assertIn("City Hotlines", nav)
        self.assertTrue(
            re.search(r'<a class="floating-nav__link floating-nav__link--action"[^>]*title="[^"]+"', nav),
            "the City Hotlines action needs a tooltip like every other item",
        )

    def test_each_link_has_a_tooltip_and_a_real_target(self):
        html, _ = self._nav()
        links = re.findall(
            r'<a class="floating-nav__link" href="#([^"]+)" title="([^"]+)"', html
        )
        self.assertTrue(links, "no section links found")
        for anchor, title in links:
            self.assertEqual(html.count(f'id="{anchor}"'), 1, f"#{anchor} has no unique target")
            self.assertTrue(title.strip(), f"#{anchor} has no tooltip text")

    def test_the_button_controls_the_section_list(self):
        html, nav = self._nav()
        self.assertIn('aria-controls="floating-nav-list"', nav)
        self.assertIn('aria-expanded="false"', nav)
        self.assertEqual(html.count('id="floating-nav-list"'), 1)

    def test_every_section_is_listed_once_for_the_scrollspy(self):
        """Every page keeps exactly one nav link per section, so the scrollspy
        has a single place to hang aria-current."""
        html, _ = self._nav()
        targets = re.findall(r'class="floating-nav__link" href="#([^"]+)"', html)
        self.assertEqual(len(targets), len(set(targets)), "a section is listed twice")

    def test_the_ring_knows_how_many_items_it_must_place(self):
        """The ring is positioned entirely in CSS from the list's item count and
        each item's index, so a missing or repeated index would stack two items
        on one spot. Every page must ship a full, ordered run: the sections, then
        the City Hotlines action."""
        for name, count in self.SECTIONS.items():
            with self.subTest(page=name):
                _, nav = self._nav(name)
                self.assertEqual(nav.count('class="floating-nav__link"'), count)
                self.assertIn(f'style="--nav-n: {count + 1}"', nav)
                for index in range(count + 1):
                    self.assertIn(f'style="--i: {index}"', nav)

    def test_the_ring_has_one_scrim_outside_the_nav(self):
        """Tap-outside closes the ring, so the scrim must be a sibling: a fixed
        element inside the nav would be trapped by the nav's stacking context."""
        html, nav = self._nav()
        self.assertEqual(html.count('class="nav-scrim"'), 1)
        self.assertNotIn("nav-scrim", nav)
        self.assertLess(
            html.index('class="floating-nav"'), html.index('class="nav-scrim"'),
            "the scrim must follow the nav in the document",
        )

    def test_the_round_button_offers_a_menu_and_a_close_icon(self):
        """Phones swap a hamburger for a close cross; the rail instead shows the
        collapse arrow. All three icons are in the markup once, toggled in CSS."""
        html, nav = self._nav()
        for icon in ("menu", "x", "chevron-left"):
            self.assertEqual(
                nav.count(f'href="#icon-{icon}"'), 1, f"#icon-{icon} should appear once"
            )

    def test_the_menu_button_is_labelled_for_screen_readers(self):
        html, nav = self._nav()
        self.assertRegex(nav, r'<span class="visually-hidden">Menu</span>')


class ActionStackTests(TestCase):
    """Back-to-top and the emergency button share one fixed stack, so they can
    never float over the page content on their own, and the stack is spaced from
    the menu button by the same gap it uses inside itself."""

    def _stack(self, html):
        match = re.search(r'<div class="action-stack">(.*?)</div>', html, re.S)
        self.assertIsNotNone(match, "no action stack rendered")
        return match.group(1)

    def test_both_floating_actions_sit_in_one_stack(self):
        html = self.client.get(reverse("about")).content.decode()
        stack = self._stack(html)
        self.assertIn("back-to-top", stack)
        self.assertIn("emergency-fab", stack)

    def test_scroll_to_top_sits_above_emergency(self):
        html = self.client.get(reverse("about")).content.decode()
        stack = self._stack(html)
        self.assertLess(
            stack.index("back-to-top"), stack.index("emergency-fab"),
            "back-to-top should stack above the emergency button",
        )

    def test_the_quick_dial_sheet_stays_out_of_the_stack(self):
        """A fixed flex column would become the dialog's containing block, so
        the sheet must remain a sibling of the stack."""
        html = self.client.get(reverse("about")).content.decode()
        self.assertNotIn("emergency-sheet", self._stack(html))

    def test_each_fixed_action_appears_once(self):
        html = self.client.get(reverse("about")).content.decode()
        self.assertEqual(html.count('class="back-to-top"'), 1)
        self.assertEqual(html.count('class="emergency-fab"'), 1)
        self.assertEqual(html.count('class="action-stack"'), 1)

    def test_emergency_and_city_hotlines_are_separate_uses_of_one_link(self):
        """Emergency stays out of navigation: only the floating button carries
        the quick-dial hook, while the menu's City Hotlines action is a plain
        link to the hotlines section of the directory."""
        html = self.client.get(reverse("about")).content.decode()
        stack = self._stack(html)
        self.assertEqual(html.count("data-emergency-open"), 1)
        self.assertIn('class="emergency-fab" href="{}"'.format(reverse("emergency")), stack)
        self.assertIn(
            'href="{}#hotlines"'.format(reverse("directory")),
            html[html.index('class="floating-nav"'):html.index('class="nav-scrim"')],
        )

    def test_the_emergency_button_keeps_a_name_without_its_label(self):
        """Phones show the Emergency button as a bare icon, so the element itself
        must still carry a name for assistive tech and a tooltip."""
        html = self.client.get(reverse("about")).content.decode()
        self.assertRegex(
            html,
            r'<a class="emergency-fab"[^>]*data-emergency-open[^>]*title="[^"]+"',
        )
        self.assertIn('class="emergency-fab__text"', html)


class FloatingActionLayoutTests(SimpleTestCase):
    """The floating chrome is laid out in CSS, so its geometry is pinned here by
    reading the stylesheets: one shared gap, one shared radius scale, and a phone
    column that stacks the three actions without overlap."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        static_dir = Path(settings.BASE_DIR) / "static" / "css"
        cls.tokens = (static_dir / "tokens.css").read_text(encoding="utf-8")
        cls.base = (static_dir / "base.css").read_text(encoding="utf-8")

    def test_the_gap_between_floating_actions_is_one_shared_token(self):
        self.assertRegex(self.tokens, r"--fab-gap:\s*1\.25rem")
        self.assertIn("gap: var(--fab-gap)", self.base)

    def test_phone_stack_clears_the_menu_button_by_one_gap(self):
        """Bottom-to-top the column must read Menu, gap, Emergency, gap,
        Back-to-top - so the stack's own bottom edge is the menu's height plus
        the shared gap above the safe area."""
        self.assertRegex(
            self.base,
            r"bottom:\s*calc\(var\(--space-4\)\s*\+\s*var\(--fab\)\s*\+\s*"
            r"var\(--fab-gap\)\s*\+\s*env\(safe-area-inset-bottom",
        )

    def test_the_three_actions_share_one_radius_and_one_shadow_scale(self):
        for selector in (r"\.emergency-fab\s*\{", r"\.back-to-top\s*\{"):
            block = re.search(selector + r"(.*?)\}", self.base, re.S)
            self.assertIsNotNone(block, f"{selector} missing from base.css")
            self.assertIn("border-radius: 999px", block.group(1))
            self.assertIn("backdrop-filter", block.group(1))
            self.assertIn("box-shadow", block.group(1))

    def test_the_menu_button_is_the_largest_of_the_three(self):
        """Hierarchy by size: the primary navigation trigger is a full --fab
        circle, the emergency button matches it, and back-to-top is the smaller
        --fab-sm."""
        self.assertRegex(self.tokens, r"--fab:\s*3\.5rem")
        self.assertRegex(self.tokens, r"--fab-sm:\s*2\.75rem")
        self.assertRegex(self.base, r"\.back-to-top\s*\{[^}]*width:\s*var\(--fab-sm\)")

    def test_the_phone_ring_radius_and_item_width_cannot_overlap(self):
        """Eight labelled items is the busiest page. At the narrowest supported
        phone the ring must keep a whole tile of clearance between neighbours and
        still fit inside the screen."""
        self.assertRegex(self.base, r"--nav-r:\s*min\(35vw,\s*8\.25rem\)")
        self.assertRegex(self.base, r"--nav-item-w:\s*min\(5rem,\s*24vw\)")

        for width in (320, 360, 375, 390, 414, 430):
            with self.subTest(width=width):
                radius = min(0.35 * width, 132)
                item = min(80, 0.24 * width)
                neighbours = 2 * radius * math.sin(math.radians(180 / 8))
                self.assertGreaterEqual(
                    neighbours, item,
                    f"{width}px: ring items would crowd each other",
                )
                self.assertLessEqual(
                    radius + item / 2, width / 2,
                    f"{width}px: the ring would run off the screen",
                )

