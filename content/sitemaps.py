"""XML sitemaps generated from the same page inventory as the navigation.

Crawlers get one canonical URL per page plus every published article, notice,
event, and public document. Dates let search engines see fresh content first.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Article, Document, Event, Notice
from .navigation import PAGES

# Pages that should not be advertised to search engines.
EXCLUDED = {"sitemap_page"}


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        names = ["home", *(name for name, _route, _title in PAGES)]
        return [name for name in names if name not in EXCLUDED]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.published()

    def lastmod(self, item):
        return item.published_at


class NoticeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Notice.objects.filter(published_at__lte=timezone.now())

    def lastmod(self, item):
        return item.published_at


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Event.objects.all()

    def lastmod(self, item):
        return item.start_datetime


class DocumentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Only documents hosted on this site: an external URL cannot be
        # prefixed with the site domain, and we do not vouch for other hosts.
        return Document.objects.filter(is_public=True, published_at__lte=timezone.now()).exclude(
            file=""
        )

    def location(self, item):
        return item.file.url

    def lastmod(self, item):
        return item.published_at
