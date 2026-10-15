"""PROTOTYPE ONLY - fake/curated content for design review on the `prototype` branch.

Content is based on the real city website (https://puertoprincesa.ph/) so the
redesign can be reviewed with realistic material: real headlines, real service
links, real festivals. Dates for news are fixed (taken from the live site);
event dates are computed from today so nothing ever looks expired.

When the redesign is approved, replace the context in content.views.home with
Article/Event/Notice/Service queries and delete this file.

External links (marked below) point at the live city site and partner portals.
"""

from datetime import date
from datetime import timedelta

# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

TAGLINE = (
    "The City Nestled Within the Heart of the Forest, "
    "Where Nature and Progress Thrive in Harmony."
)

# Hotlinked from the live site for the prototype only. Replace with a local
# static image (static/img/) before launch.
LOGO_URL = "https://puertoprincesa.ph/wp-content/uploads/2025/08/PPC-LOGO-PNG.png"

FACEBOOK_URL = "https://www.facebook.com/puertoprincesaph"

# ---------------------------------------------------------------------------
# Advisory banner (example content, replace with real advisories)
# ---------------------------------------------------------------------------

URGENT_NOTICE = {
    "title": "Water service interruption in selected barangays",
    "summary": (
        f"Scheduled maintenance of the main water line will interrupt service in "
        f"Barangays Poblacion, Banilad, and Mandaragat on "
        f"{timedelta(days=1) and (date.today() + timedelta(days=1)):%d} to "
        f"{(date.today() + timedelta(days=2)):%d %B}. Store enough water in advance."
    ),
    "link_label": "Read the full advisory",
    "href": "https://puertoprincesa.ph/notices-and-announcements/",
}

# ---------------------------------------------------------------------------
# Online services - real links to city portals and offices (from the live site)
# ---------------------------------------------------------------------------

# Top row of quick cards.
EPORTALS = [
    {
        "name": "e-Payment",
        "description": "Access online payment services.",
        "icon": "credit-card",
        "href": "https://www.filipizen.com/partners/palawan_puertoprincesa",
    },
    {
        "name": "CGPP Service Desk",
        "description": "Submit and track service requests.",
        "icon": "life-buoy",
        "href": "https://cgpp.online/servicerequest",
    },
    {
        "name": "Legislative Tracking System",
        "description": "Monitor legislative information.",
        "icon": "landmark",
        "href": "https://puertoprincesa.ph/legislative-tracking-system/",
    },
]

# City offices and attractions with their own online services.
SERVICES = [
    {
        "name": "City Building and Occupancy Permits",
        "description": "Building-related services and permits.",
        "icon": "building",
        "href": "https://ocbo.puertoprincesa.ph/",
    },
    {
        "name": "City Tourism",
        "description": "Discover Puerto Princesa tourism.",
        "icon": "map-pin",
        "href": "https://citytourism.puertoprincesa.ph/",
    },
    {
        "name": "Bids and Awards",
        "description": "Procurement and bidding information.",
        "icon": "file-text",
        "href": "https://bacoffice.puertoprincesa.ph/",
    },
    {
        "name": "City Planning Office",
        "description": "Planning and development information.",
        "icon": "compass",
        "href": "https://sites.google.com/view/ppcplanningdepartment/home?authuser=0",
    },
    {
        "name": "Puerto Princesa Underground River",
        "description": "Explore the city's world-famous attraction.",
        "icon": "waves",
        "href": "https://undergroundriver.puertoprincesa.ph/",
    },
]

# ---------------------------------------------------------------------------
# Underground River feature section (facts from the live site)
# ---------------------------------------------------------------------------

RIVER_FACTS = [
    # "value"/"suffix" drive the count-up animation; value None = show as-is.
    {"stat": "8.2 km", "label": "Total length of the underground river", "value": 8.2, "suffix": " km"},
    {"stat": "4.3 km", "label": "Navigable section of the river", "value": 4.3, "suffix": " km"},
    {"stat": "1 of 7", "label": "New7Wonders of Nature", "value": None, "suffix": ""},
    {"stat": "1999", "label": "UNESCO Heritage Site designation", "value": 1999, "suffix": ""},
    {"stat": "100+", "label": "Unique wildlife species", "value": 100, "suffix": "+"},
    {"stat": "20M+ years", "label": "Age of limestone formations", "value": 20, "suffix": "M+ years"},
]

# ---------------------------------------------------------------------------
# Emergency quick-dial (PROTOTYPE numbers for the design demo only).
# 911 and the City Hall switchboard are real; the rest are placeholders that
# must be replaced with the verified Directory numbers before launch.
# ---------------------------------------------------------------------------

EMERGENCY_CONTACTS = [
    {
        "name": "National Emergency Hotline",
        "number": "911",
        "digits": "911",
        "note": "Police, fire, and ambulance - nationwide",
    },
    {
        "name": "City Government switchboard",
        "number": "(048) 717-8000",
        "digits": "+63487178000",
        "note": "City Hall - ask for CDRRMO or the office you need",
    },
    {
        "name": "Disaster response and rescue (CDRRMO)",
        "number": "(048) 433-2470",
        "digits": "+63484332470",
        "note": "Typhoon, flood, and rescue operations",
    },
    {
        "name": "Puerto Princesa City Police Station",
        "number": "(048) 433-2104",
        "digits": "+63484332104",
        "note": "Police assistance and peace and order",
    },
    {
        "name": "Palawan Provincial Hospital",
        "number": "(048) 434-2126",
        "digits": "+63484342126",
        "note": "Public hospital emergency room",
    },
]

# ---------------------------------------------------------------------------
# Mayor's Corner (profile from the live site)
# ---------------------------------------------------------------------------

MAYOR = {
    "name": "Hon. Lucilo R. Bayron",
    "title": "City Mayor",
    "photo": "https://puertoprincesa.ph/wp-content/uploads/2025/08/mayor-bayron.png",
    "blurb": (
        "Known as The Action Man of Puerto Princesa City, Mayor Bayron initiated "
        "programs guided by the motto: Hindi Bukas, Kundi Ngayon - not tomorrow, "
        "but today."
    ),
    "href": "https://puertoprincesa.ph/new-mayors-corner/",
}

# ---------------------------------------------------------------------------
# News (recent headlines from the City Information Office, live site)
# ---------------------------------------------------------------------------

NEWS = [
    {
        "category": "Articles",
        "title": "New regional director of Commission on Population and Development-MIMAROPA pays courtesy call on Mayor Bayron",
        "summary": (
            "The new regional director introduced himself to the mayor and discussed "
            "joint programs, praising the city's vision and its mini-City Halls that "
            "bring services closer to residents."
        ),
        "author": "Charlito Christopher Padul, CIO",
        "date": date(2026, 10, 12),
        "href": "https://puertoprincesa.ph/articles/bagong-regional-director-ng-commission-on-population-and-development-mimaropa-nag-courtesy-visit-kay-mayor-bayron/",
    },
    {
        "category": "Articles",
        "title": "PHLPost Acting Area Director pays courtesy call on Mayor Bayron",
        "summary": (
            "Postal officials discussed PHLPost services with the city, including the "
            "Postal ID, stamps, mailing, and parcel delivery."
        ),
        "author": "Charlito Christopher Padul, CIO",
        "date": date(2026, 10, 12),
        "href": "https://puertoprincesa.ph/articles/phlpost-acting-area-director-pays-courtesy-call-on-mayor-bayron/",
    },
    {
        "category": "Articles",
        "title": "City institutionalizes quarterly allowance for teachers and non-teaching staff",
        "summary": (
            "On final reading, the City Council approved the institutionalization of "
            "the 6,000-peso quarterly allowance for teachers and non-teaching personnel "
            "under DepEd Puerto Princesa."
        ),
        "author": "City Council / CIO",
        "date": date(2026, 10, 6),
        "href": "https://puertoprincesa.ph/articles/",
    },
]

# ---------------------------------------------------------------------------
# Notices to the Public (live site headlines)
# ---------------------------------------------------------------------------

NOTICES = [
    {
        "title": "City Assessor's Office services, now closer to residents",
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Puerto Princesa City Mental Health and Wellness Clinic, open to the public",
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Sunburn: do not underestimate it - it is serious skin damage too",
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
]

# ---------------------------------------------------------------------------
# Upcoming events (from the live site events page; dates computed so the
# prototype never shows expired items)
# ---------------------------------------------------------------------------

TODAY = date.today()


def _ahead(days):
    return TODAY + timedelta(days=days)


EVENTS = [
    {
        "title": "Fun Fishing Day at Balayong People's Park",
        "date": _ahead(8),
        "time": "6:00 AM",
        "venue": "Balayong People's Park",
        "href": "https://puertoprincesa.ph/events/fun-fishing-day/",
    },
    {
        "title": "The Philippine Beach Games Puerto Princesa media launch",
        "date": _ahead(15),
        "time": "4:00 PM",
        "venue": "The Dome Hotel, Puerto Princesa",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Blessing and inauguration of the Screaming Eagle Zipline",
        "date": _ahead(22),
        "time": "8:00 AM",
        "venue": "Balayong People's Park",
        "href": "https://puertoprincesa.ph/events/",
    },
]

# ---------------------------------------------------------------------------
# Festival calendar (real city festivals and their traditional dates)
# ---------------------------------------------------------------------------

FESTIVALS = [
    ("Jan 1", "Bagong Taon Bagong Buhay sa Baybay", "New Year celebration at the City Baywalk"),
    ("Feb 14", "Love Affair with Nature", "Mangrove planting and nature activities"),
    ("Mar 4", "Balayong Festival", "Citywide celebration of the Palawan cherry"),
    ("Apr", "Pangalipay sa Baybay", "Week of coastal festivities after the fiesta"),
    ("May 1", "Karagatan Festival", "Month of the Ocean celebration"),
    ("Jun", "Pista y ang Cagueban", "Forest festival and tree planting for the youth"),
]

# ---------------------------------------------------------------------------
# Honors and seals (logos hotlinked from the live site for the prototype)
# ---------------------------------------------------------------------------

SEALS = [
    ("https://puertoprincesa.ph/wp-content/uploads/2025/08/image-removebg-preview.png", "City Government seal"),
    ("https://puertoprincesa.ph/wp-content/uploads/2025/08/ppur_final.png", "Puerto Princesa Underground River brand mark"),
    ("https://puertoprincesa.ph/wp-content/uploads/2025/08/iso.png", "ISO certification mark"),
    ("https://puertoprincesa.ph/wp-content/uploads/2025/08/download-1.png", "Award seal"),
    ("https://puertoprincesa.ph/wp-content/uploads/2025/08/download.png", "Award seal"),
]
