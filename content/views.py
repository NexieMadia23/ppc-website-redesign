from django.shortcuts import render

from content import prototype_data


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


def placeholder(request, title):
    """Temporary page so every menu/footer link works until its real step is built."""
    return render(request, "placeholder.html", {"page_title": title})


def search(request):
    return render(request, "search.html", {"q": request.GET.get("q", "").strip()})
