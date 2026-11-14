import re

from django.conf import settings
from django.urls import reverse

# PROTOTYPE ONLY: emergency quick-dial data for the homepage dialog.
# Remove this import and the EMERGENCY_CONTACTS entry below when the redesign
# is merged into main and the real Directory data is wired up.
from . import prototype_data
from .navigation import GOV_LINKS, MAIN_MENU, UTILITY_LINKS


def _menu_link(entry):
    """Turn a navigation entry into a label + working URL."""
    if entry.get("name"):
        url = reverse(entry["name"])
        if entry.get("anchor"):
            url = f"{url}#{entry['anchor']}"
        return label_url(entry["label"], url, external=False)
    return label_url(entry["label"], entry["url"], external=True)


def label_url(label, url, external):
    return {"label": label, "url": url, "external": external}


def site(request):
    match = getattr(request, "resolver_match", None)
    current = match.url_name if match else None
    phone = settings.SITE_PHONE

    nav_items = []
    for item in MAIN_MENU:
        link = _menu_link(item)
        nav_items.append(
            {
                **link,
                "is_current": item.get("name") == current,
                "children": [_menu_link(child) for child in item.get("children", [])],
            }
        )

    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": getattr(settings, "SITE_URL", "http://127.0.0.1:8001"),
        "SITE_PHONE": phone,
        "SITE_PHONE_HREF": re.sub(r"[^\d+]", "", phone),
        "SITE_EMAIL": settings.SITE_EMAIL,
        "NAV_ITEMS": nav_items,
        "UTILITY_LINKS": UTILITY_LINKS,
        "GOV_LINKS": GOV_LINKS,
        # Pages with their own prominent search box keep the header one out
        # of the way, so a visitor never sees two search fields at once.
        "HIDE_HEADER_SEARCH": current in {"home", "search"},
        "EMERGENCY_CONTACTS": prototype_data.EMERGENCY_CONTACTS,
        "PHOTO_CREDITS": prototype_data.PHOTO_CREDITS,
        "PHOTO_CREDIT_AUTHORS": list(
            dict.fromkeys(item["author"] for item in prototype_data.PHOTO_CREDITS)
        ),
    }
