"""Resolve the photo shown on an event detail page.

Uploaded photos always win. The three official event photos downloaded for the
prototype are kept locally under ``static/img/banner/`` as fallbacks, so the page
never hotlinks a third-party image host.
"""

from django.templatetags.static import static

# Official event photos from the city's own event pages.
EVENT_IMAGE_FALLBACKS = {
    "fun-fishing-day-at-balayong-peoples-park": {
        "stem": "img/banner/fun-fishing-day",
        "alt": "Residents and guests at the Fun Fishing Day in Balayong People's Park.",
    },
    "the-philippine-beach-games-puerto-princesa-media-launch": {
        "stem": "img/banner/philippine-beach-games",
        "alt": "The Philippine Beach Games Puerto Princesa media launch at The Dome Hotel.",
    },
    "blessing-and-inauguration-of-the-screaming-eagle-zipline": {
        "stem": "img/banner/screaming-eagle-zipline",
        "alt": "The Screaming Eagle Zipline at Balayong People's Park.",
    },
}

# Used when an unmapped event has no image of its own.
GENERIC_IMAGE = (
    "img/photos/hero-baywalk",
    "Sunrise over the Puerto Princesa City Baywalk.",
)


def _static_image(stem, alt):
    return {
        "url": static(f"{stem}.jpg"),
        "webp": static(f"{stem}.webp"),
        "alt": alt,
    }


def event_image(event):
    """Return the image data used by the event detail page."""
    if event.image:
        return {"url": event.image.url, "webp": "", "alt": event.image_alt}
    fallback = EVENT_IMAGE_FALLBACKS.get(event.slug)
    if fallback:
        return _static_image(fallback["stem"], fallback["alt"])
    return _static_image(*GENERIC_IMAGE)


def event_card_image(event):
    """Photo for a listing card, or None when the event has no official image.

    Listings do not borrow the generic detail-page hero: an event with no
    photo of its own shows the date tile instead of another event's picture.
    """
    if isinstance(event, dict):
        fallback = EVENT_IMAGE_FALLBACKS.get(event.get("slug"))
    elif event.image:
        return {"url": event.image.url, "webp": "", "alt": event.image_alt}
    else:
        fallback = EVENT_IMAGE_FALLBACKS.get(event.slug)
    if not fallback:
        return None
    return _static_image(fallback["stem"], fallback["alt"])
