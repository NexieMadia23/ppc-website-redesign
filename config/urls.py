from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from content import views
from content.navigation import PAGES

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
    path("admin/", admin.site.urls),
]

for name, route, title in PAGES:
    if name in PAGE_VIEWS:
        urlpatterns.append(path(route, PAGE_VIEWS[name], name=name))
    else:
        urlpatterns.append(path(route, views.placeholder, {"title": title}, name=name))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
