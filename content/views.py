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
    }
    return render(request, "home.html", context)


def placeholder(request, title):
    """Temporary page so every menu/footer link works until its real step is built."""
    return render(request, "placeholder.html", {"page_title": title})


def search(request):
    return render(request, "search.html", {"q": request.GET.get("q", "").strip()})
