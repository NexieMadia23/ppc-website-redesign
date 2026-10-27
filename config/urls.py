from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.templatetags.static import static as static_url
from django.urls import path
from django.views.generic import RedirectView

from content import views
from content.navigation import PAGES
from content.sitemaps import NewsSitemap, StaticViewSitemap

SITEMAPS = {"pages": StaticViewSitemap, "news": NewsSitemap}

# Pages with a real (prototype) view. Everything else in PAGES still gets a
# working placeholder so no menu or footer link can ever 404.
PAGE_VIEWS = {
    "about": views.about,
    "government": views.government,
    "tourism": views.tourism,
    "directory": views.directory,
    "emergency": views.emergency,
    "news": views.news,
    "contact": views.contact,
    "transparency": views.transparency,
    "privacy": views.privacy,
    "accessibility": views.accessibility,
    "sitemap_page": views.sitemap_page,
    "foi": views.foi,
}

urlpatterns = [
    path("", views.home, name="home"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("search/", views.search, name="search"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("admin/", admin.site.urls),
]

for name, route, title in PAGES:
    if name in PAGE_VIEWS:
        urlpatterns.append(path(route, PAGE_VIEWS[name], name=name))
    else:
        urlpatterns.append(path(route, views.placeholder, {"title": title}, name=name))

# Browsers and crawlers still ask for /favicon.ico directly. Point it at the
# real icon (the official city logo) so the tab never falls back to a 404.
urlpatterns.append(
    path("favicon.ico", RedirectView.as_view(url=static_url("favicon.ico"), permanent=True))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
