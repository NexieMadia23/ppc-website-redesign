"""Crawl the public site and report broken internal links.

This is the automated version of the "all links must work" promise. It starts
from every public page listed in ``content.navigation.PAGES`` plus the core
routes, follows internal links it finds in the HTML, and fails when a page or
asset returns 404/500.

Run it locally with ``python manage.py check_links`` and in CI with
``--fail-on-error``.
"""

from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit

from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.urls import NoReverseMatch, reverse

from content.navigation import PAGES

# Staff tools and uploaded files are not part of the public crawl.
SKIP_PREFIXES = ("/admin/", "/dashboard/", "/logout/", "/static/", "/media/")
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data", "sms"}
MAX_PAGES = 200


class LinkParser(HTMLParser):
    """Collect every href/action on a page."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"a", "area", "form"}:
            return
        attributes = dict(attrs)
        if tag == "form":
            # A POST form is submitted by the browser, never fetched like a
            # page. Requesting it with GET would report a false 405.
            method = (attributes.get("method") or "get").strip().lower()
            if method != "get":
                return
            action = attributes.get("action")
            if action:
                self.links.append(action)
            return
        for key in ("href", "action"):
            value = attributes.get(key)
            if value:
                self.links.append(value)


def start_urls():
    names = ["home", "search", "sumbungan", "complaint_track", "faq", "photo_credits"]
    names += [name for name, _route, _title in PAGES]
    urls = ["/"]
    for name in names:
        try:
            url = reverse(name)
        except NoReverseMatch:
            continue
        if url not in urls:
            urls.append(url)
    urls.append("/search/?q=permit")
    return urls


def clean_url(value, base):
    """Return an internal path with query, or ``None`` when it is out of scope."""
    raw = (value or "").strip()
    if not raw or raw.startswith("#"):
        return None
    parts = urlsplit(raw)
    if parts.scheme.lower() in SKIP_SCHEMES:
        return None
    if parts.scheme and parts.scheme not in {"http", "https"}:
        return None

    absolute = urljoin(base, raw)
    parts = urlsplit(absolute)
    if parts.netloc and parts.netloc.split(":")[0] not in {"localhost", "testserver"}:
        return None

    path = parts.path or "/"
    if path.startswith(SKIP_PREFIXES):
        return None
    if path.endswith((".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico", ".pdf", ".zip")):
        # Assets are checked by the browser build; do not fetch binaries here.
        return None
    return urlunsplit(("", "", path, parts.query, ""))


class Command(BaseCommand):
    help = "Crawl public pages and report broken internal links."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fail-on-error",
            action="store_true",
            help="Exit with a non-zero status when any link is broken.",
        )
        parser.add_argument(
            "--max-pages",
            type=int,
            default=MAX_PAGES,
            help=f"Maximum pages to request (default: {MAX_PAGES}).",
        )

    def handle(self, *args, **options):
        client = Client(SERVER_NAME="localhost")
        base = "http://localhost"
        queue = list(start_urls())
        seen = set()
        broken = []
        checked = 0

        while queue and checked < options["max_pages"]:
            target = queue.pop(0)
            if target in seen:
                continue
            seen.add(target)
            checked += 1

            try:
                response = client.get(target, follow=False)
            except Exception as error:  # noqa: BLE001 - report, do not stop the crawl
                broken.append((target, f"error: {error}"))
                continue

            if response.status_code >= 400:
                broken.append((target, str(response.status_code)))
                continue

            if response.status_code in {301, 302, 307, 308}:
                location = response.headers.get("Location", "")
                next_url = clean_url(location, base + target)
                if next_url and next_url not in seen:
                    queue.append(next_url)
                continue

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            parser = LinkParser()
            try:
                parser.feed(response.content.decode(response.charset or "utf-8", errors="replace"))
            except Exception:  # noqa: BLE001 - malformed HTML should not crash CI
                continue
            for href in parser.links:
                next_url = clean_url(href, base + target)
                if next_url and next_url not in seen:
                    queue.append(next_url)

        for url, reason in broken:
            self.stdout.write(self.style.ERROR(f"BROKEN  {url}  ({reason})"))

        if broken:
            summary = f"{len(broken)} broken link(s) across {checked} page(s)."
            if options["fail_on_error"]:
                raise CommandError(summary)
            self.stdout.write(self.style.WARNING(summary))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"No broken internal links across {checked} page(s).")
            )
