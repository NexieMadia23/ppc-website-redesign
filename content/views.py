from django.http import Http404
from django.shortcuts import render

from content import prototype_data
from content.navigation import MAIN_NAV, PAGES


def home(request):
    """Homepage.

    On the `prototype` branch the context comes from content.prototype_data
    (fake content for design review). When the design is approved, swap these
    for real Article/Event/Notice/Service queries and delete prototype_data.
    """
    context = {
        "tagline": prototype_data.TAGLINE,
        "urgent_notice": prototype_data.URGENT_NOTICE,
        "eportals": prototype_data.EPORTALS,
        "services": prototype_data.SERVICES,
        "river_facts": prototype_data.RIVER_FACTS,
        "mayor": prototype_data.MAYOR,
        "news": prototype_data.NEWS,
        "notices": prototype_data.NOTICES,
        "events": prototype_data.EVENTS,
        "festivals": prototype_data.FESTIVALS,
        "seals": prototype_data.SEALS,
        "sidebar_sections": prototype_data.HOMEPAGE_SIDEBAR,
    }
    return render(request, "home.html", context)


def about(request):
    """About our city (prototype page)."""
    context = {
        "profile": prototype_data.CITY_PROFILE,
        "facts": prototype_data.CITY_FACTS,
        "history": prototype_data.HISTORY_POINTS,
        "sidebar_sections": prototype_data.ABOUT_SIDEBAR,
    }
    return render(request, "about.html", context)


def government(request):
    """Government overview (prototype page)."""
    context = {
        "pillars": prototype_data.GOVERNMENT_PILLARS,
        "mayor": prototype_data.MAYOR,
        "departments": prototype_data.DEPARTMENTS,
        "sidebar_sections": prototype_data.GOVERNMENT_SIDEBAR,
    }
    return render(request, "government.html", context)


def tourism(request):
    """Tourism (prototype page)."""
    context = {
        "attractions": prototype_data.ATTRACTIONS,
        "river_facts": prototype_data.RIVER_FACTS,
        "festivals": prototype_data.FESTIVALS,
        "travel_tips": prototype_data.TRAVEL_TIPS,
        "sidebar_sections": prototype_data.TOURISM_SIDEBAR,
    }
    return render(request, "tourism.html", context)


def directory(request):
    """Directory of offices and contacts (prototype page)."""
    context = {
        "emergency_contacts": prototype_data.EMERGENCY_CONTACTS,
        "offices": prototype_data.DIRECTORY_OFFICES,
        "sidebar_sections": prototype_data.DIRECTORY_SIDEBAR,
    }
    return render(request, "directory.html", context)


def emergency(request):
    """Emergency contacts (prototype page)."""
    context = {
        "emergency_contacts": prototype_data.EMERGENCY_CONTACTS,
        "safety_tips": prototype_data.SAFETY_TIPS,
        "sidebar_sections": prototype_data.EMERGENCY_SIDEBAR,
    }
    return render(request, "emergency.html", context)


def news(request):
    """News and updates listing (prototype page)."""
    context = {
        "articles": prototype_data.NEWS_ARTICLES,
        "notices": prototype_data.NOTICES,
        "events": prototype_data.EVENTS,
        "sidebar_sections": prototype_data.NEWS_SIDEBAR,
    }
    return render(request, "news.html", context)


def news_detail(request, slug):
    """A single news article (prototype page)."""
    article = next((item for item in prototype_data.NEWS_ARTICLES if item["slug"] == slug), None)
    if article is None:
        raise Http404("Article not found")
    related = [item for item in prototype_data.NEWS_ARTICLES if item["slug"] != slug][:3]
    context = {
        "article": article,
        "related": related,
        "sidebar_sections": prototype_data.ARTICLE_SIDEBAR,
    }
    return render(request, "news_detail.html", context)


def contact(request):
    """Contact page with a prototype form (prototype page)."""
    context = {
        "details": prototype_data.CONTACT_DETAILS,
        "topics": prototype_data.CONTACT_TOPICS,
        "faqs": prototype_data.CONTACT_FAQS,
        "sidebar_sections": prototype_data.CONTACT_SIDEBAR,
    }
    return render(request, "contact.html", context)


def transparency(request):
    """Full Disclosure / transparency (prototype page)."""
    context = {
        "groups": prototype_data.TRANSPARENCY_GROUPS,
        "sidebar_sections": prototype_data.TRANSPARENCY_SIDEBAR,
    }
    return render(request, "transparency.html", context)


def privacy(request):
    """Privacy policy (prototype page)."""
    context = {
        "sections": prototype_data.PRIVACY_SECTIONS,
        "details": prototype_data.CONTACT_DETAILS,
        "sidebar_sections": prototype_data.PRIVACY_SIDEBAR,
    }
    return render(request, "privacy.html", context)


def accessibility(request):
    """Accessibility statement (prototype page)."""
    context = {
        "features": prototype_data.ACCESSIBILITY_FEATURES,
        "sections": prototype_data.ACCESSIBILITY_SECTIONS,
        "details": prototype_data.CONTACT_DETAILS,
        "sidebar_sections": prototype_data.ACCESSIBILITY_SIDEBAR,
    }
    return render(request, "accessibility.html", context)


def sitemap_page(request):
    """Site map, generated from the same list that builds the menu."""
    context = {
        "main_nav": MAIN_NAV,
        "pages": [(name, title) for name, _route, title in PAGES],
        "sidebar_sections": prototype_data.SITEMAP_SIDEBAR,
    }
    return render(request, "sitemap.html", context)


def foi(request):
    """Freedom of Information (prototype page)."""
    context = {
        "requests": prototype_data.FOI_REQUESTS,
        "steps": prototype_data.FOI_STEPS,
        "exceptions": prototype_data.FOI_EXCEPTIONS,
        "details": prototype_data.CONTACT_DETAILS,
        "sidebar_sections": prototype_data.FOI_SIDEBAR,
    }
    return render(request, "foi.html", context)


def placeholder(request, title):
    """Temporary page so every menu/footer link works until its real step is built."""
    return render(request, "placeholder.html", {"page_title": title})


def search(request):
    return render(request, "search.html", {"q": request.GET.get("q", "").strip()})


def robots_txt(request):
    """Crawler rules. Keep private and non-canonical paths out of the index."""
    return render(request, "robots.txt", content_type="text/plain")
