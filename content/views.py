from io import BytesIO
from uuid import uuid4

from django.contrib import messages
from django.core.files.base import ContentFile
from django.db import connection
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from PIL import Image, ImageOps, UnidentifiedImageError

from content import prototype_data
from content.article_images import article_image
from content.event_images import event_card_image, event_image
from content.faq import FAQS, find_answer
from content.forms import ComplaintForm, ContactForm
from content.models import (
    Agency,
    Article,
    Complaint,
    ComplaintAttachment,
    ComplaintUpdate,
    Document,
    Event,
    FaqQuery,
    Feedback,
    Notice,
    Office,
    Service,
)
from content.navigation import MAIN_NAV, PAGES
from content.ratelimit import is_limited

# ---------------------------------------------------------------------------
# Database rows -> template-ready cards
#
# Templates were written against prototype dicts. These small adapters keep the
# template markup readable while every card now comes from the database.
# ---------------------------------------------------------------------------


def _excerpt(text, limit=180):
    """Shorten prose at a word boundary so a summary never ends mid-word."""
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def _service_groups(cards):
    """Bucket service cards into the resident task groups, in a fixed order."""
    groups = []
    for key, label in prototype_data.SERVICE_GROUPS:
        items = [card for card in cards if card.get("task") == key]
        if items:
            groups.append({"key": key, "label": label, "items": items})
    return groups


def _article_card(article):
    if isinstance(article, dict):
        return {
            **article,
            "photo": article_image(article),
        }

    shown_category = article.get_category_display()
    for item in prototype_data.NEWS_ARTICLES:
        if item["slug"] == article.slug:
            shown_category = item["category"]
            break

    return {
        "title": article.title,
        "slug": article.slug,
        "summary": article.summary,
        "category": shown_category,
        "date": article.published_at,
        "author": "City Information Office",
        "image": article.image,
        "image_alt": article.image_alt,
        "photo": article_image(article),
    }


def _notice_card(notice):
    return {
        "title": notice.title,
        "slug": notice.slug,
        "summary": _excerpt(notice.body),
        "body": notice.body,
        "date": notice.published_at,
        "is_urgent": notice.is_urgent,
        "href": notice.get_absolute_url(),
    }


def _event_card(event):
    # Read the clock in the city's timezone; the stored value is UTC, so
    # strftime on it would print a time that disagrees with the local date.
    start = timezone.localtime(event.start_datetime)
    # A midnight start means the time was never recorded; show the date alone
    # rather than a misleading "12:00 AM".
    has_time = (start.hour, start.minute) != (0, 0)
    return {
        "title": event.title,
        "slug": event.slug,
        "summary": event.description,
        "date": start,
        "time": start.strftime("%I:%M %p").lstrip("0") if has_time else "",
        "venue": event.venue,
        "contact": event.contact,
        "href": event.get_absolute_url(),
        "photo": event_card_image(event),
    }


def _prototype_event_cards():
    return [
        {
            **item,
            "external": item["href"].startswith("http"),
            "photo": event_card_image(item),
        }
        for item in prototype_data.EVENTS
    ]


def _service_card(service):
    return {
        "name": service.name,
        "description": service.description,
        "icon": service.icon or "life-buoy",
        "href": service.url,
        "external": service.is_external,
        "task": prototype_data.SERVICE_TASKS.get(service.name, "know"),
    }


def home(request):
    """Homepage: published database content first, prototype content as fallback.

    Every public listing uses the same published-only rules, so a future-dated
    article or notice can be scheduled in the admin and simply appears on time.
    """
    now = timezone.now()
    articles = list(Article.objects.published()[:3])
    notices = list(Notice.objects.filter(published_at__lte=now)[:3])
    events = list(Event.objects.filter(start_datetime__gte=now)[:3])
    services = list(Service.objects.all())
    urgent = (
        Notice.objects.filter(published_at__lte=now, is_urgent=True)
        .order_by("-published_at")
        .first()
    )

    if services:
        service_cards = [_service_card(item) for item in services]
    else:
        service_cards = [
            {**item, "external": item["href"].startswith("http")}
            for item in prototype_data.EPORTALS + prototype_data.SERVICES
        ]
    seen = set()
    unique_services = []
    for card in service_cards:
        if card["name"] not in seen:
            seen.add(card["name"])
            unique_services.append(card)

    context = {
        "tagline": prototype_data.TAGLINE,
        # Only a real, published, urgent notice can raise the advisory banner.
        # With nothing in the database the banner stays away instead of showing
        # example text that would read as a live emergency.
        "urgent_notice": (
            {
                "title": urgent.title,
                "summary": urgent.body,
                "href": urgent.get_absolute_url(),
                "link_label": "Read the full advisory",
                "external": False,
            }
            if urgent
            else None
        ),
        "service_groups": _service_groups(unique_services),
        "river_facts": prototype_data.RIVER_FACTS,
        "mayor": prototype_data.MAYOR,
        "news": (
            [_article_card(item) for item in articles]
            if articles
            else [_article_card(item) for item in prototype_data.NEWS]
        ),
        "notices": (
            [_notice_card(item) for item in notices] if notices else prototype_data.NOTICES
        ),
        "events": ([_event_card(item) for item in events] if events else _prototype_event_cards()),
        "festivals": prototype_data.FESTIVALS,
        "seals": prototype_data.SEALS,
        "city_photos": prototype_data.CITY_PHOTOS,
        "hero_slides": prototype_data.HERO_SLIDES,
        "sidebar_sections": prototype_data.HOMEPAGE_SIDEBAR,
    }
    return render(request, "home.html", context)


def about(request):
    """About our city (prototype page)."""
    barangays = prototype_data.CITY_BARANGAYS
    context = {
        "profile": prototype_data.CITY_PROFILE,
        "highlights": prototype_data.CITY_PROFILE_HIGHLIGHTS,
        "facts": prototype_data.CITY_FACTS,
        "barangays": barangays,
        # One dot per barangay, grouped so the map of dots shows the split.
        "urban_dots": range(barangays["urban"]),
        "rural_dots": range(barangays["rural"]),
        "journeys": prototype_data.CITY_JOURNEYS,
        "culture": prototype_data.CITY_CULTURE,
        "city_photos": prototype_data.CITY_PHOTOS,
        "history": prototype_data.HISTORY_POINTS,
        "sidebar_sections": prototype_data.ABOUT_SIDEBAR,
    }
    return render(request, "about.html", context)


# The prototype department list and the seeded directory use a few different
# spellings for the same office. Map the variants so each department can show
# its real line instead of a generic card.
DEPARTMENT_OFFICE_ALIASES = {
    "City Engineer's Office": "City Engineering Office",
    "City Agriculturist's Office": "City Agriculture Office",
}


def government(request):
    """Government overview, with department rows linked to real contacts."""
    query = request.GET.get("q", "").strip()
    offices = {
        office.name: office
        for office in Office.objects.exclude(is_emergency=True).prefetch_related("services")
    }
    switchboard = offices.get("City Hall switchboard")
    departments = []
    for dept in prototype_data.DEPARTMENTS:
        office = offices.get(DEPARTMENT_OFFICE_ALIASES.get(dept["name"], dept["name"]))
        if query and query.lower() not in f"{dept['name']} {dept['blurb']}".lower():
            continue
        phone_source = office or switchboard
        departments.append(
            {
                "name": dept["name"],
                "blurb": dept["blurb"],
                "phone": phone_source.phone if phone_source else "",
                "digits": (
                    phone_source.phone_digits or phone_source.phone
                    if phone_source
                    else ""
                ),
                "email": office.email if office else "",
                "slug": office.slug if office else "",
                "contact_label": "Office line" if office else "City Hall switchboard",
            }
        )

    context = {
        "pillars": prototype_data.GOVERNMENT_PILLARS,
        "mayor": prototype_data.MAYOR,
        "departments": departments,
        "department_query": query,
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


def _office_card(office):
    """Normalise a DB Office (or a prototype dict) for the directory template."""
    if isinstance(office, dict):
        return {
            "name": office["name"],
            "slug": office["name"].lower().replace(" ", "-"),
            "phone": office.get("phone") or office.get("number", ""),
            "digits": office.get("digits", ""),
            "email": office.get("email", ""),
            "note": office.get("note", ""),
            "agency": "",
            "address": "",
            "hours": office.get("hours", ""),
            "services": [],
        }
    return {
        "name": office.name,
        "slug": office.slug,
        "phone": office.phone,
        "digits": office.phone_digits or office.phone,
        "email": office.email,
        "note": office.description,
        "agency": office.agency.name if office.agency else "",
        "address": office.address,
        "hours": office.hours,
        "services": [service.name for service in office.services.all()],
    }


def directory(request):
    """Office directory backed by the database, with a prototype fallback."""
    query = request.GET.get("q", "").strip()
    agency = request.GET.get("agency", "").strip()

    db_offices = Office.objects.select_related("agency").prefetch_related("services")
    if db_offices.exists():
        emergency = [_office_card(item) for item in db_offices.filter(is_emergency=True)]
        offices = db_offices.filter(is_emergency=False)
        if query:
            offices = offices.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(email__icontains=query)
                | Q(agency__name__icontains=query)
                | Q(services__name__icontains=query)
            ).distinct()
        if agency:
            offices = offices.filter(agency_id=agency)
        offices = [_office_card(item) for item in offices]
    else:
        emergency = [_office_card(item) for item in prototype_data.EMERGENCY_CONTACTS]
        offices = [
            _office_card(item)
            for item in prototype_data.DIRECTORY_OFFICES
            if not query or query.lower() in f"{item['name']} {item.get('note', '')}".lower()
        ]

    context = {
        "emergency_contacts": emergency,
        "offices": offices,
        "query": query,
        "agency": agency,
        "agencies": Agency.objects.filter(offices__isnull=False).distinct(),
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
    """News and updates listing, driven by the database."""
    now = timezone.now()
    articles = list(Article.objects.published()[:12])
    notices = list(Notice.objects.filter(published_at__lte=now)[:8])
    events = list(Event.objects.filter(start_datetime__gte=now)[:8])

    context = {
        "articles": (
            [_article_card(item) for item in articles]
            if articles
            else [_article_card(item) for item in prototype_data.NEWS_ARTICLES]
        ),
        "notices": (
            [_notice_card(item) for item in notices] if notices else prototype_data.NOTICES
        ),
        "events": ([_event_card(item) for item in events] if events else _prototype_event_cards()),
        "sidebar_sections": prototype_data.NEWS_SIDEBAR,
    }
    return render(request, "news.html", context)


def news_detail(request, slug):
    """A single news article, from the database first then prototype data."""
    article_obj = Article.objects.published().filter(slug=slug).first()
    if article_obj is not None:
        article = _article_card(article_obj)
        article["body"] = [line for line in article_obj.body.split("\n") if line.strip()]
        related = [
            _article_card(item)
            for item in Article.objects.published().exclude(pk=article_obj.pk)[:3]
        ]
    else:
        # A future-dated draft must not open early, even with the right slug.
        if Article.objects.filter(slug=slug).exists():
            raise Http404("Article not found")
        article = next(
            (item for item in prototype_data.NEWS_ARTICLES if item["slug"] == slug),
            None,
        )
        if article is None:
            raise Http404("Article not found")
        article = {**article, "photo": article_image(article)}
        related = [
            {**item, "photo": article_image(item)}
            for item in prototype_data.NEWS_ARTICLES
            if item["slug"] != slug
        ][:3]
    context = {
        "article": article,
        "related": related,
        "sidebar_sections": prototype_data.ARTICLE_SIDEBAR,
    }
    return render(request, "news_detail.html", context)


def notice_detail(request, slug):
    """A public notice, with future-dated notices kept hidden."""
    notice = get_object_or_404(Notice.objects.filter(published_at__lte=timezone.now()), slug=slug)
    related = Notice.objects.filter(
        published_at__lte=timezone.now(), is_urgent=notice.is_urgent
    ).exclude(pk=notice.pk)[:3]
    context = {
        "notice": notice,
        "related": related,
        "sidebar_sections": prototype_data.NEWS_SIDEBAR,
    }
    return render(request, "notice_detail.html", context)


def event_detail(request, slug):
    """A single city event."""
    event = get_object_or_404(Event, slug=slug)
    related = Event.objects.filter(start_datetime__gte=timezone.now()).exclude(pk=event.pk)[:3]
    context = {
        "event": event,
        "hero_image": event_image(event),
        "related": related,
        "sidebar_sections": prototype_data.NEWS_SIDEBAR,
    }
    return render(request, "event_detail.html", context)


def contact(request):
    """Contact page; saves messages for staff follow-up."""
    topics = prototype_data.CONTACT_TOPICS
    form = ContactForm(request.POST or None, topics=topics)
    if request.method == "POST":
        if is_limited(request, "contact"):
            messages.error(
                request,
                "Too many messages were sent from this device. Please wait a few "
                "minutes and try again, or call City Hall.",
            )
        elif form.is_valid():
            form.save()
            messages.success(
                request,
                "Salamat! Your message has been received. The City Information "
                "Office will reply to the email address you provided.",
            )
            return redirect("contact")
    context = {
        "details": prototype_data.CONTACT_DETAILS,
        "topics": topics,
        "faqs": prototype_data.CONTACT_FAQS,
        "form": form,
        "sidebar_sections": prototype_data.CONTACT_SIDEBAR,
    }
    return render(request, "contact.html", context)


def transparency(request):
    """Full Disclosure / transparency, with database documents taking over."""
    documents = list(Document.objects.filter(is_public=True, published_at__lte=timezone.now()))
    if documents:
        meta = {
            Document.Category.BUDGET: (
                "landmark",
                "How the city raises and spends public money.",
            ),
            Document.Category.BIDS: (
                "file-text",
                "Procurement notices, awards, and contracts.",
            ),
            Document.Category.ORDINANCE: (
                "book",
                "Ordinances, resolutions, and the rules behind city services.",
            ),
            Document.Category.REPORT: (
                "chart",
                "Performance, accomplishment, and monitoring reports.",
            ),
            Document.Category.FOI: (
                "shield",
                "Documents released through the Freedom of Information programme.",
            ),
            Document.Category.OTHER: ("file-text", "Other public documents."),
        }
        groups = []
        for value, label in Document.Category.choices:
            items = [item for item in documents if item.category == value]
            if not items:
                continue
            icon, blurb = meta.get(value, ("file-text", ""))
            groups.append(
                {
                    "id": value,
                    "name": label,
                    "icon": icon,
                    "blurb": blurb,
                    "items": [
                        {
                            "name": item.title,
                            "note": item.description
                            or f"{item.year} · {item.get_category_display()}",
                            "year": item.year,
                            "status": item.get_status_display(),
                            "status_key": item.status,
                            "href": item.href if item.is_available else "",
                            "external": bool(item.external_url and not item.file),
                        }
                        for item in items
                    ],
                }
            )
    else:
        groups = prototype_data.TRANSPARENCY_GROUPS

    context = {
        "groups": groups,
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
    nav_names = {name for name, _label in MAIN_NAV}
    context = {
        "main_nav": MAIN_NAV,
        "other_pages": [
            (name, title) for name, _route, title in PAGES if name not in nav_names
        ],
        "sidebar_sections": prototype_data.SITEMAP_SIDEBAR,
    }
    return render(request, "sitemap.html", context)


def foi(request):
    """Freedom of Information (prototype page)."""
    context = {
        "requests": prototype_data.FOI_REQUESTS,
        "steps": prototype_data.FOI_STEPS,
        "exceptions": prototype_data.FOI_EXCEPTIONS,
        "details": prototype_data.FOI_DETAILS,
        "sidebar_sections": prototype_data.FOI_SIDEBAR,
    }
    return render(request, "foi.html", context)


def placeholder(request, title):
    """Temporary page so every menu/footer link works until its real step is built."""
    return render(request, "placeholder.html", {"page_title": title})


def photo_credits(request):
    """Attribution page for every local photograph used on the site."""
    return render(
        request,
        "photo_credits.html",
        {
            "credits": prototype_data.PHOTO_CREDITS,
            "sidebar_sections": None,
        },
    )


def search(request):
    """Multimodal search: typed text, voice (Web Speech API on the client), and
    category filters. Results come from the same models the public pages use,
    with prototype data as a fallback when the database is empty."""
    query = request.GET.get("q", "").strip()
    kind = request.GET.get("type", "").strip()

    all_results = _search_results(query) if query else []
    counts = {}
    for item in all_results:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1

    results = [item for item in all_results if item["kind"] == kind] if kind else all_results

    context = {
        "q": query,
        "kind": kind,
        "results": results,
        "total": len(results),
        "all_total": len(all_results),
        "counts": counts,
        "kind_choices": [(name, counts[name]) for name in SEARCH_KIND_ORDER if counts.get(name)],
        "popular": ["business permit", "birth certificate", "street light", "emergency"],
        "faq_suggestions": FAQS[:3],
        "sidebar_sections": None,
    }
    return render(request, "search.html", context)


SEARCH_KIND_ORDER = [
    "Service",
    "Office",
    "News",
    "Event",
    "Notice",
    "Document",
    "FAQ",
    "Page",
]

PAGE_DESCRIPTIONS = {
    "about": "City profile, history, and facts about Puerto Princesa.",
    "government": "Departments, officials, and the structure of city government.",
    "tourism": "Attractions, festivals, and travel tips for visitors.",
    "news": "News, notices, and upcoming events from City Hall.",
    "transparency": "Budgets, bids, ordinances, and public documents.",
    "directory": "Emergency hotlines and contact details for city offices.",
    "contact": "City Hall address, switchboard, email, and office hours.",
    "emergency": "Emergency hotlines and safety tips.",
    "privacy": "How the city handles personal information.",
    "accessibility": "Accessibility features and how to use them.",
    "sitemap_page": "Every page on this website in one place.",
    "foi": "How to request public documents through FOI.",
    "faq": "Answers to common questions about city services and this site.",
}


def _search_results(query):
    q = query.lower()
    results = []

    def add(kind, title, description, url, icon, external=False, meta=""):
        results.append(
            {
                "kind": kind,
                "title": title,
                "description": description,
                "url": url,
                "icon": icon,
                "external": external,
                "meta": meta,
            }
        )

    # Services (database, then prototype fallback).
    services = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))[:10]
    if services:
        for item in services:
            add(
                "Service",
                item.name,
                item.description,
                item.url,
                item.icon or "life-buoy",
                external=item.is_external,
            )
    else:
        for item in prototype_data.EPORTALS + prototype_data.SERVICES:
            if q in f"{item['name']} {item['description']}".lower():
                add(
                    "Service",
                    item["name"],
                    item["description"],
                    item["href"],
                    item.get("icon", "life-buoy"),
                    external=item["href"].startswith("http"),
                )

    # Offices (database, then prototype fallback).
    offices = Office.objects.select_related("agency").filter(
        Q(name__icontains=q) | Q(description__icontains=q) | Q(agency__name__icontains=q)
    )[:10]
    if offices:
        for item in offices:
            description = item.description or (item.agency.name if item.agency else "")
            add(
                "Office",
                item.name,
                description,
                reverse("directory") + f"#office-{item.slug}",
                "building",
                meta=item.phone,
            )
    else:
        for item in prototype_data.DIRECTORY_OFFICES:
            if q in f"{item['name']} {item.get('note', '')}".lower():
                add(
                    "Office",
                    item["name"],
                    item.get("note", ""),
                    reverse("directory"),
                    "building",
                    meta=item.get("phone", ""),
                )

    # News articles.
    articles = Article.objects.published().filter(
        Q(title__icontains=q) | Q(summary__icontains=q) | Q(body__icontains=q)
    )[:10]
    if articles:
        for item in articles:
            add(
                "News",
                item.title,
                item.summary,
                reverse("news_detail", args=[item.slug]),
                "file-text",
                meta=item.published_at.strftime("%b %d, %Y"),
            )
    else:
        for item in prototype_data.NEWS_ARTICLES:
            if q in f"{item['title']} {item['summary']}".lower():
                add(
                    "News",
                    item["title"],
                    item["summary"],
                    reverse("news_detail", args=[item["slug"]]),
                    "file-text",
                    meta=item["date"].strftime("%b %d, %Y"),
                )

    # Events.
    events = Event.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q) | Q(venue__icontains=q)
    )[:10]
    if events:
        for item in events:
            add(
                "Event",
                item.title,
                _excerpt(item.description),
                item.get_absolute_url(),
                "calendar",
                meta=item.start_datetime.strftime("%b %d, %Y"),
            )
    else:
        for item in prototype_data.EVENTS:
            if q in f"{item['title']} {item['venue']}".lower():
                add(
                    "Event",
                    item["title"],
                    f"At {item['venue']}.",
                    reverse("news") + "#events",
                    "calendar",
                    meta=item["date"].strftime("%b %d, %Y"),
                )

    # Notices.
    notices = Notice.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q),
        published_at__lte=timezone.now(),
    )[:10]
    if notices:
        for item in notices:
            add(
                "Notice",
                item.title,
                _excerpt(item.body),
                item.get_absolute_url(),
                "alert",
                meta=item.published_at.strftime("%b %d, %Y"),
            )
    else:
        for item in prototype_data.NOTICES:
            if q in item["title"].lower():
                add(
                    "Notice",
                    item["title"],
                    "",
                    reverse("news") + "#notices",
                    "alert",
                )

    # Transparency documents.
    for item in Document.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))[:10]:
        add(
            "Document",
            item.title,
            item.description,
            item.href or reverse("transparency"),
            "download",
            external=bool(item.external_url),
            meta=str(item.year),
        )

    # FAQs.
    for item in FAQS:
        haystack = f"{item['question']} {item['answer']} {' '.join(item['keywords'])}"
        if q in haystack.lower():
            add(
                "FAQ",
                item["question"],
                _excerpt(item["answer"]),
                reverse("faq") + f"#faq-{item['id']}",
                "message",
            )

    # Static pages.
    for name, _route, title in PAGES:
        description = PAGE_DESCRIPTIONS.get(name, "")
        if q in f"{title} {description}".lower():
            add("Page", title, description, reverse(name), "compass")

    order = {kind: index for index, kind in enumerate(SEARCH_KIND_ORDER)}
    results.sort(key=lambda item: (order.get(item["kind"], 99), item["title"].lower()))
    return results


def faq(request):
    """FAQ page. The same list powers the chatbot, so answers stay in sync."""
    groups = []
    seen = []
    for item in FAQS:
        if item["category"] not in seen:
            seen.append(item["category"])
            groups.append(
                {
                    "category": item["category"],
                    "items": [faq for faq in FAQS if faq["category"] == item["category"]],
                }
            )
    context = {
        "groups": groups,
        "faqs": FAQS,
        "sidebar_sections": None,
    }
    return render(request, "faq.html", context)


@require_GET
def faq_ask(request):
    """Answer an assistant question by matching the city's FAQ.

    No AI service is involved. Unmatched questions are logged so the content
    team can write the missing answer, and the endpoint is rate limited so the
    cache and database cannot be filled by a bot.
    """
    if is_limited(request, "faq"):
        return JsonResponse(
            {
                "ok": False,
                "error": "You are asking very quickly. Please wait a moment and try again.",
            },
            status=429,
        )

    message = request.GET.get("q", "").strip()[:500]
    match = find_answer(message)
    if match:
        return JsonResponse(
            {
                "ok": True,
                "question": match["question"],
                "answer": match["answer"],
                "url": reverse(match["link"][0]) if match.get("link") else "",
                "link_label": match["link"][1] if match.get("link") else "",
            }
        )

    if len(message) >= 4:
        FaqQuery.objects.create(question=message)

    return JsonResponse(
        {
            "ok": True,
            "answer": (
                "I don't have a ready answer for that yet. You can browse the FAQ, "
                "or file a Sumbungan ng Bayan request and the city will route it to "
                "the right office."
            ),
            "url": reverse("faq"),
            "link_label": "Browse the FAQ",
        }
    )


# ---------------------------------------------------------------------------
# Sumbungan ng Bayan (public complaint and request system)
# ---------------------------------------------------------------------------


def _store_attachments(complaint, uploads):
    """Re-encode photos as WebP and drop EXIF/GPS metadata.

    Uploads are already type/size checked by the form. A corrupt image is
    skipped rather than allowed to break the resident's submission.
    """
    stored = 0
    for upload in uploads[:3]:
        try:
            with Image.open(upload) as source:
                source.load()
                image = ImageOps.exif_transpose(source)
                if image.mode in {"RGBA", "LA", "P"}:
                    image = image.convert("RGBA")
                    canvas = Image.new("RGB", image.size, (255, 255, 255))
                    canvas.paste(image, mask=image.split()[-1])
                    image = canvas
                else:
                    image = image.convert("RGB")
                image.thumbnail((1600, 1600))
                buffer = BytesIO()
                image.save(buffer, format="WEBP", quality=82, method=4)
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
            continue

        data = buffer.getvalue()
        ComplaintAttachment.objects.create(
            complaint=complaint,
            file=ContentFile(data, name=f"{uuid4().hex}.webp"),
            original_name=(upload.name or "photo")[:255],
            content_type="image/webp",
            size=len(data),
        )
        stored += 1
    return stored


def sumbungan(request):
    """Public complaint form. Residents do not need an account."""
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if is_limited(request, "sumbungan"):
            messages.error(
                request,
                "Too many requests were sent from this device. Please wait a few "
                "minutes and try again, or call the Sumbungan hotline.",
            )
        elif form.is_valid():
            complaint = form.save(commit=False)
            if complaint.is_anonymous:
                complaint.name = ""
                complaint.email = ""
                complaint.phone = ""
            complaint.agency = Agency.objects.filter(category=complaint.category).first()
            complaint.save()
            photos = _store_attachments(complaint, form.cleaned_data.get("attachments") or [])
            note = "Request received through the Sumbungan ng Bayan form."
            if photos:
                note += f" {photos} photo(s) attached."
            ComplaintUpdate.objects.create(
                complaint=complaint,
                status=Complaint.Status.RECEIVED,
                note=note,
            )
            messages.success(
                request,
                f"Received. Your reference number is {complaint.reference}. Keep it to track your request.",
            )
            return redirect("complaint_track_detail", reference=complaint.reference)
    else:
        form = ComplaintForm()

    context = {
        "form": form,
        "categories": Complaint.Category.choices,
        "agencies": Agency.objects.all(),
        "sidebar_sections": None,
    }
    return render(request, "sumbungan.html", context)


def complaint_track(request):
    """Look up a complaint by reference number."""
    reference = request.POST.get("reference", "").strip().upper()
    if request.method == "POST":
        if is_limited(request, "track"):
            messages.error(
                request,
                "Too many lookups from this device. Please wait a few minutes and try again.",
            )
        elif not reference:
            messages.error(request, "Enter the reference number from your confirmation.")
        elif Complaint.objects.filter(reference=reference).exists():
            return redirect("complaint_track_detail", reference=reference)
        else:
            messages.error(
                request,
                "We could not find that reference. Check the number and try again.",
            )
    context = {"reference": reference, "sidebar_sections": None}
    return render(request, "complaint_track.html", context)


def complaint_track_detail(request, reference):
    """Public status page for one complaint. Contact details are never shown."""
    complaint = get_object_or_404(
        Complaint.objects.select_related("agency"),
        reference=reference.strip().upper(),
    )
    context = {
        "complaint": complaint,
        "updates": complaint.updates.filter(is_public=True),
        "attachments": complaint.attachments.all(),
        "sidebar_sections": None,
    }
    return render(request, "complaint_track_detail.html", context)


@require_POST
def submit_feedback(request):
    """Store a 'was this page helpful?' response from any public page."""
    page = (request.POST.get("page") or request.POST.get("next") or "/").strip()[:200]
    helpful_raw = (request.POST.get("helpful") or "").strip().lower()
    comment = (request.POST.get("comment") or "").strip()[:2000]

    # A filled honeypot is a bot. Pretend it worked so it does not retry.
    if request.POST.get("website"):
        if _wants_json(request):
            return JsonResponse({"ok": True, "message": "Salamat!"})
        return redirect(_safe_next(request, page))

    if is_limited(request, "feedback"):
        if _wants_json(request):
            return JsonResponse(
                {"ok": False, "error": "Too many responses. Please try again later."},
                status=429,
            )
        messages.error(request, "Too many responses from this device. Please try again later.")
        return redirect(_safe_next(request, page))

    if helpful_raw not in {"1", "0", "yes", "no", "true", "false"}:
        if _wants_json(request):
            return JsonResponse({"ok": False, "error": "Choose yes or no."}, status=400)
        messages.error(request, "Choose whether the page was helpful.")
        return redirect(_safe_next(request, page))

    helpful = helpful_raw in {"1", "yes", "true"}
    Feedback.objects.create(page=page, helpful=helpful, comment=comment)

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "message": "Salamat! Your feedback helps us improve this page.",
            }
        )

    messages.success(request, "Salamat! Your feedback helps us improve this page.")
    return redirect(_safe_next(request, page))


def _wants_json(request):
    return request.headers.get(
        "x-requested-with"
    ) == "XMLHttpRequest" or "application/json" in request.headers.get("accept", "")


def _safe_next(request, fallback="/"):
    from django.utils.http import url_has_allowed_host_and_scheme

    target = request.POST.get("next") or fallback
    if target.startswith("/") and not target.startswith("//"):
        return target
    if url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return target
    return "/"


def robots_txt(request):
    """Crawler rules. Keep private and non-canonical paths out of the index."""
    return render(request, "robots.txt", content_type="text/plain")


def healthz(request):
    """Railway health check. Fail fast when the database is unreachable."""
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "error"}, status=503)
    return JsonResponse({"status": "ok"})


def page_not_found(request, exception):
    """Branded 404 that does not repeat the header search field."""
    return render(request, "404.html", {"hide_header_search": True}, status=404)
