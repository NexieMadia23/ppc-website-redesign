import re

from django.conf import settings
from django.urls import reverse

# PROTOTYPE ONLY: emergency quick-dial data for the homepage dialog.
# Remove this import and the EMERGENCY_CONTACTS entry below when the redesign
# is merged into main and the real Directory data is wired up.
from . import prototype_data
from .navigation import GOV_LINKS, MAIN_NAV


def site(request):
    match = getattr(request, "resolver_match", None)
    current = match.url_name if match else None
    phone = settings.SITE_PHONE
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "SITE_PHONE": phone,
        # tel: links must contain digits only (and a leading +)
        "SITE_PHONE_HREF": re.sub(r"[^\d+]", "", phone),
        "SITE_EMAIL": settings.SITE_EMAIL,
        "NAV_ITEMS": [
            {"label": label, "url": reverse(name), "is_current": name == current}
            for name, label in MAIN_NAV
        ],
        "GOV_LINKS": GOV_LINKS,
        "EMERGENCY_CONTACTS": prototype_data.EMERGENCY_CONTACTS,
    }
