from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.templatetags.static import static as static_url
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from content import views
from content.navigation import PAGES
from content.redirects import legacy_urlpatterns
from content.sitemaps import (
    DocumentSitemap,
    EventSitemap,
    NewsSitemap,
    NoticeSitemap,
    StaticViewSitemap,
)

SITEMAPS = {
    "pages": StaticViewSitemap,
    "news": NewsSitemap,
    "notices": NoticeSitemap,
    "events": EventSitemap,
    "documents": DocumentSitemap,
}

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
    "faq": views.faq,
}

urlpatterns = [
    path("", views.home, name="home"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("notices/<slug:slug>/", views.notice_detail, name="notice_detail"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("search/", views.search, name="search"),
    path("photo-credits/", views.photo_credits, name="photo_credits"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("healthz/", views.healthz, name="healthz"),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("sumbungan/", views.sumbungan, name="sumbungan"),
    path("sumbungan/track/", views.complaint_track, name="complaint_track"),
    path(
        "sumbungan/track/<str:reference>/",
        views.complaint_track_detail,
        name="complaint_track_detail",
    ),
    path("feedback/", views.submit_feedback, name="submit_feedback"),
    path("faq/ask/", views.faq_ask, name="faq_ask"),
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

# Old WordPress addresses, redirected permanently to their new pages.
urlpatterns += legacy_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # WhiteNoise serves STATIC_ROOT, not user uploads. Keep complaint photos and
    # other media reachable in production; a Railway volume or object storage
    # handles persistence.
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

handler404 = "content.views.page_not_found"
