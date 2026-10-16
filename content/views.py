from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from content import prototype_data
from content.models import Article, Event, Notice, Service
from content.navigation import MAIN_NAV, PAGES


def home(request):
    """Homepage.

    News, notices, events and services come from the database. The rest of the
    homepage (city facts, festivals, seals) still comes from content.prototype_data
    until those pages get their models - see the README follow-ups.
    """
    context = {
        "tagline": prototype_data.TAGLINE,
        "urgent_notice": Notice.objects.filter(is_urgent=True).first(),
        "eportals": Service.objects.filter(section=Service.Section.PORTALS),
        "services": Service.objects.filter(section=Service.Section.OFFICES),
        "river_facts": prototype_data.RIVER_FACTS,
        "mayor": prototype_data.MAYOR,
        "news": Article.objects.published()[:3],
        "notices": Notice.objects.filter(is_urgent=False)[:3],
        "events": Event.objects.upcoming()[:3],
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
    """News listing: published articles, newest first.

    `?page=` paginates and `?category=` filters by the CIO's section. Both are
    query parameters rather than extra URLs, so the menu and the generated site
    map stay unchanged.
    """
    articles = Article.objects.published()
    used = set(articles.values_list("category", flat=True).distinct())
    categories = [
        (value, label) for value, label in Article.Category.choices if value in used
    ]

    active = request.GET.get("category", "").strip()
    if active not in used:
        active = ""
    if active:
        articles = articles.filter(category=active)

    paginator = Paginator(articles, settings.NEWS_PER_PAGE)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "articles": page.object_list,
        "page_obj": page,
        "paginator": paginator,
        "categories": categories,
        "active_category": active,
        "notices": Notice.objects.filter(is_urgent=False),
        "events": Event.objects.upcoming(),
        "sidebar_sections": prototype_data.NEWS_SIDEBAR,
    }
    return render(request, "news.html", context)


def news_detail(request, slug):
    """A single published article. Future-dated articles 404 like unknown ones."""
    article = get_object_or_404(Article.objects.published(), slug=slug)
    related = Article.objects.published().exclude(pk=article.pk)[:3]
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
