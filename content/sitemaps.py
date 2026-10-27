"""XML sitemaps generated from the same page inventory as the navigation.

Crawlers get one canonical URL per page plus every published news article, so a
new page added to ``content/navigation.py`` is discoverable automatically.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import prototype_data
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
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return prototype_data.NEWS_ARTICLES

    def location(self, article):
        return reverse("news_detail", args=[article["slug"]])

    def lastmod(self, article):
        return article["date"]
