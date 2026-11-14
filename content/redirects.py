"""Permanent redirects for the old WordPress site.

The live city site (puertoprincesa.ph) publishes deep links that residents,
search engines, and printed materials still use. Instead of letting those
addresses 404 after the redesign, each old path is matched here and sent to the
closest page in the new structure with a 301.

Keep this list small and explicit. Do not redirect the whole site: only paths
that used to exist and still have a sensible destination.
"""

from django.urls import re_path
from django.views.generic import RedirectView

# (old path pattern, new URL name). Patterns are matched without the leading
# slash, and the first matching rule wins.
LEGACY_REDIRECTS = [
    # WordPress categories and archives.
    (r"^category/.*$", "news"),
    (r"^tag/.*$", "news"),
    (r"^author/.*$", "news"),
    (r"^\d{4}/\d{2}/?$", "news"),
    (r"^latest-events-information-tab(?:/.*)?$", "news"),
    (r"^notices-and-announcements(?:/.*)?$", "news"),
    (r"^news-and-updates(?:/.*)?$", "news"),
    (r"^feed/?$", "news"),
    # Pages that existed on the old site under a different name.
    (r"^about-us/?$", "about"),
    (r"^city-government/?$", "government"),
    (r"^city-officials/?$", "government"),
    (r"^departments/?$", "directory"),
    (r"^offices/?$", "directory"),
    (r"^services/?$", "directory"),
    (r"^downloadable-documents/?$", "transparency"),
    (r"^full-disclosure(?:-policy)?/?$", "transparency"),
    (r"^transparency-seal/?$", "transparency"),
    (r"^citizens-charter/?$", "transparency"),
    (r"^tourist-spots/?$", "tourism"),
    (r"^contact-us/?$", "contact"),
    (r"^city-emergency-contacts/?$", "emergency"),
    (r"^privacy-policy/?$", "privacy"),
    (r"^site-map/?$", "sitemap_page"),
    (r"^sitemap/?$", "sitemap_page"),
]


def legacy_urlpatterns():
    """Return the redirect routes, ready to append to ``urlpatterns``."""
    return [
        re_path(pattern, RedirectView.as_view(pattern_name=name, permanent=True))
        for pattern, name in LEGACY_REDIRECTS
    ]
