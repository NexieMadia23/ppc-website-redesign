"""Resolve the photo shown on a news card and article page.

Uploaded photos always win. For the prototype, official city photos are stored
locally under ``static/img/news/`` and mapped to article slugs, so the site
never hotlinks a third-party image host.
"""

from django.templatetags.static import static

# Official City Government of Puerto Princesa photos, used with credit on the
# photo credits page. Keys match Article.slug in prototype_data / the database.
ARTICLE_IMAGE_FALLBACKS = {
    "subaraw-festival-queen-2026": {
        "stem": "img/news/subaraw-queen",
        "alt": "Subaraw Festival Queen 2026 candidates on stage at the Edward S. Hagedorn Coliseum.",
    },
    "subaraw-biodiversity-festival-2026-success": {
        "stem": "img/news/subaraw-success",
        "alt": "Mayor Lucilo Bayron joins the Subaraw Biodiversity Festival 2026 closing program.",
    },
    "subaraw-national-hiphop-dance-competition-2026": {
        "stem": "img/news/subaraw-hiphop",
        "alt": "Dancers perform at the Subaraw National Hiphop Dance Competition 2026.",
    },
    "city-peso-bread-making-training": {
        "stem": "img/news/bread-training",
        "alt": "Women in Barangay Masikap join the City Peso bread-making skills training.",
    },
    "subaraw-drum-and-lyre-competition": {
        "stem": "img/news/drum-and-lyre",
        "alt": "A school drum and lyre band performs during the Subaraw Biodiversity Festival.",
    },
    "subaraw-national-music-championship-2027": {
        "stem": "img/news/music-championship",
        "alt": "Drum and lyre performers at the Subaraw festival in Puerto Princesa.",
    },
    "subaraw-festival-grows-as-national-event": {
        "stem": "img/news/subaraw-national",
        "alt": "Mayor Lucilo Bayron speaks at the Subaraw Biodiversity Festival 2026.",
    },
    "new-school-stage-tagburos-elementary": {
        "stem": "img/news/school-stage",
        "alt": "The newly inaugurated stage at Tagburos Elementary School.",
    },
    "subaraw-biodiversity-festival-grand-opening": {
        "stem": "img/news/subaraw-opening",
        "alt": "The Subaraw Biodiversity Festival 2026 grand opening at the coliseum.",
    },
    "subaraw-2026-preserving-nature": {
        "stem": "img/news/subaraw-sabang",
        "alt": "The Subaraw Biodiversity Festival opens in Sitio Sabang, Barangay Cabayugan.",
    },
    "bfp-courtesy-call-mayor-bayron": {
        "stem": "img/news/bfp-courtesy",
        "alt": "BFP Puerto Princesa personnel meet Mayor Bayron before their ASEAN Summit deployment.",
    },
}


def _static_image(stem, alt):
    return {
        "url": static(f"{stem}.jpg"),
        "webp": static(f"{stem}.webp"),
        "alt": alt,
    }


def article_image(article):
    """Return the image data used by a news card or article hero."""
    image = getattr(article, "image", None)
    if image:
        return {
            "url": image.url,
            "webp": "",
            "alt": getattr(article, "image_alt", ""),
        }
    slug = article.get("slug") if isinstance(article, dict) else article.slug
    fallback = ARTICLE_IMAGE_FALLBACKS.get(slug)
    if fallback:
        return _static_image(fallback["stem"], fallback["alt"])
    return None
