from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from content import views
from content.navigation import PAGES

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("admin/", admin.site.urls),
]

# Placeholder pages (replaced one by one in later steps)
urlpatterns += [
    path(route, views.placeholder, {"title": title}, name=name)
    for name, route, title in PAGES
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
