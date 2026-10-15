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

# Headlines are taken from the City Information Office feed on the live site and
# rewritten in plain text. The live site fakes bold with Unicode glyphs, which
# breaks screen readers, search engines, and copy-paste, so the prototype drops
# that trick and uses real markup instead.

NEWS_ARTICLES = [
    {
        "slug": "cpd-mimaropa-courtesy-visit",
        "category": "City government",
        "title": "New regional director of CPD-MIMAROPA pays courtesy call on Mayor Bayron",
        "summary": (
            "The new regional director introduced himself to the mayor and discussed "
            "joint programs, praising the city's vision and its mini-City Halls that "
            "bring services closer to residents."
        ),
        "author": "Charlito Christopher Padul, CIO",
        "date": date(2026, 10, 12),
        "body": [
            "The new regional director of the Commission on Population and Development (CPD) for MIMAROPA paid a courtesy call on Mayor Lucilo R. Bayron at the City Mayor's Office to formally introduce himself and open coordination with the city government.",
            "\"Napaka-impressive po ng vision niyo para sa siyudad,\" the director said, citing the city's mini-City Halls, which bring frontline services closer to residents in the barangays.",
            "The meeting covered population and development programs, including family planning services, adolescent sexual and reproductive health, and the use of population data in city planning.",
            "Both offices agreed to formalize the partnership through a memorandum of agreement covering joint activities, data sharing, and community outreach in the city's barangays.",
        ],
    },
    {
        "slug": "phlpost-courtesy-call-mayor-bayron",
        "category": "City government",
        "title": "PHLPost Acting Area Director pays courtesy call on Mayor Bayron",
        "summary": (
            "Postal officials discussed PHLPost services with the city, including the "
            "Postal ID, stamps, mailing, and parcel delivery."
        ),
        "author": "Charlito Christopher Padul, CIO",
        "date": date(2026, 10, 12),
        "body": [
            "Philippine Postal Corporation (PHLPost) Acting Area Director Rosemarie N. Tubal of Postal Area 3-Mega Manila, together with other PHLPost officials, paid a courtesy call on Mayor Lucilo R. Bayron at the City Mayor's Office.",
            "The officials discussed PHLPost services, including the Postal ID, postage stamps, mailing, and parcel delivery, and how these can reach residents in the city's island and upland barangays.",
            "Mayor Bayron raised the possibility of a postal service desk during barangay outreach activities, so residents can apply for a Postal ID without travelling to the city centre.",
        ],
    },
    {
        "slug": "mayor-bayron-welcomes-tourism-interns",
        "category": "Tourism",
        "title": "Mayor Bayron welcomes tourism interns from LPU-Batangas",
        "summary": (
            "Fourteen graduating BS Tourism students from LPU-Batangas begin their "
            "internship with the city, the university's fifth batch since 2024."
        ),
        "author": "Charlito Christopher Padul, CIO",
        "date": date(2026, 10, 12),
        "body": [
            "Mayor Lucilo R. Bayron welcomed 14 graduating BS Tourism students from the Lyceum of the Philippines University (LPU)-Batangas during a courtesy call, together with two students from Luzviminda National High School who will undergo work immersion.",
            "The LPU-Batangas students make up the university's fifth batch of interns in the city since 2024.",
            "The interns will be assigned to the City Tourism Office, where they will assist with visitor services, tour accreditation, and preparations for the city's festivals.",
        ],
    },
    {
        "slug": "quarterly-allowance-for-teachers",
        "category": "City Council",
        "title": "City institutionalizes quarterly allowance for teachers and non-teaching staff",
        "summary": (
            "On final reading, the City Council approved the institutionalization of "
            "the 6,000-peso quarterly allowance for teachers and non-teaching personnel "
            "under DepEd Puerto Princesa."
        ),
        "author": "City Council / CIO",
        "date": date(2026, 10, 6),
        "body": [
            "On third and final reading, the Sangguniang Panlungsod approved the institutionalization of a 6,000-peso quarterly allowance for teachers and non-teaching personnel under the Department of Education (DepEd) Puerto Princesa.",
            "Majority Floor Leader Hon. Jonjie Rodriguez reported the approval, noting that the measure turns a discretionary benefit into a standing obligation of the city government.",
            "The allowance covers qualified teaching and non-teaching staff of public elementary and secondary schools in the city.",
        ],
    },
    {
        "slug": "macarascas-clinic-digital-xray",
        "category": "Health",
        "title": "Macarascas satellite and diagnostic clinic gets its own digital X-ray machine",
        "summary": (
            "The new digital X-ray machine and clinical laboratory expand health "
            "services for residents in the city's southern barangays."
        ),
        "author": "Maya Estandian, CIO",
        "date": date(2026, 7, 8),
        "body": [
            "The city government commissioned a new digital X-ray machine and clinical laboratory at the Macarascas Satellite and Diagnostic Clinic, expanding health services for residents in the south of the city.",
            "Before the upgrade, patients from southern barangays had to travel to the city centre for imaging and laboratory work.",
            "The clinic now offers laboratory services and faster imaging, part of the city's drive to bring health care closer to every barangay.",
        ],
    },
    {
        "slug": "nutrition-month-2026",
        "category": "Health",
        "title": "Ika-52 pagdiriwang ng Nutrition Month sa Puerto Princesa, umarangkada",
        "summary": (
            "The City Nutrition Division of the City Health Office launched the 52nd "
            "Nutrition Month celebration at the RVM Sports Complex."
        ),
        "author": "Maya Estandian, CIO",
        "date": date(2026, 7, 13),
        "body": [
            "Pormal nang inilunsad ng City Nutrition Division ng City Health Office ang pagdiriwang ng ika-52 Nutrition Month sa RVM Sports Complex noong Hulyo 10.",
            "Sa kabila ng malakas na ulan, naging matagumpay ang programa na dinaluhan ng mga barangay health worker, nutrition scholar, at mga magulang.",
            "Kabilang sa mga aktibidad ang cooking contest gamit ang lokal na gulay, feeding program, at pagpapayo sa tamang nutrisyon para sa mga bata.",
        ],
    },
]

# Homepage teaser: the latest three articles.
NEWS = [
    {
        "category": article["category"],
        "title": article["title"],
        "summary": article["summary"],
        "author": article["author"],
        "date": article["date"],
        "slug": article["slug"],
    }
    for article in NEWS_ARTICLES[:3]
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

# Festival calendar (real city festivals and their traditional dates).
# Each festival renders as a card whose date badge shows the month plus either
# the exact day or, for festivals with no fixed date, the part of the month it
# falls in ("when"), so the badge reads naturally as "Mar 4" / "Apr Week 1".
FESTIVALS = [
    {"month": "Jan", "when": "1", "name": "Bagong Taon Bagong Buhay sa Baybay",
     "blurb": "New Year celebration at the City Baywalk"},
    {"month": "Feb", "when": "14", "name": "Love Affair with Nature",
     "blurb": "Mangrove planting and nature activities"},
    {"month": "Mar", "when": "4", "name": "Balayong Festival",
     "blurb": "Citywide celebration of the Palawan cherry"},
    {"month": "Apr", "when": "Week 1", "name": "Pangalipay sa Baybay",
     "blurb": "Week of coastal festivities after the fiesta"},
    {"month": "May", "when": "1", "name": "Karagatan Festival",
     "blurb": "Month of the Ocean celebration"},
    {"month": "Jun", "when": "4th Sat", "name": "Pista y ang Cagueban",
     "blurb": "Forest festival and tree planting for the youth"},
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

# ---------------------------------------------------------------------------
# Sidebar rails (icon + label per section). The desktop glass sidebar and the
# mobile sticky bar are both rendered from these lists by base.html.
# ---------------------------------------------------------------------------

HOMEPAGE_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "online-services", "label": "Services", "icon": "credit-card"},
    {"id": "underground-river", "label": "Underground River", "icon": "waves"},
    {"id": "mayor", "label": "Mayor", "icon": "users"},
    {"id": "news", "label": "News", "icon": "file-text"},
    {"id": "events", "label": "Events", "icon": "calendar"},
    {"id": "honors", "label": "Honors", "icon": "award"},
]

ABOUT_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "profile", "label": "Profile", "icon": "info"},
    {"id": "facts", "label": "Key facts", "icon": "award"},
    {"id": "history", "label": "History", "icon": "book"},
]

GOVERNMENT_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "pillars", "label": "Overview", "icon": "landmark"},
    {"id": "council", "label": "The Mayor", "icon": "users"},
    {"id": "departments", "label": "Departments", "icon": "building"},
]

TOURISM_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "attractions", "label": "Attractions", "icon": "map-pin"},
    {"id": "river", "label": "Underground River", "icon": "waves"},
    {"id": "festivals", "label": "Festivals", "icon": "calendar"},
    {"id": "tips", "label": "Travel tips", "icon": "info"},
]

DIRECTORY_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "hotlines", "label": "Emergency", "icon": "alert"},
    {"id": "offices", "label": "City offices", "icon": "building"},
]

EMERGENCY_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "hotlines", "label": "Hotlines", "icon": "phone"},
    {"id": "safety", "label": "Safety tips", "icon": "shield"},
]

NEWS_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "latest", "label": "Latest", "icon": "file-text"},
    {"id": "notices", "label": "Notices", "icon": "alert"},
    {"id": "events", "label": "Events", "icon": "calendar"},
]

ARTICLE_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "article", "label": "Article", "icon": "file-text"},
    {"id": "related", "label": "More news", "icon": "book"},
]

CONTACT_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "details", "label": "Details", "icon": "info"},
    {"id": "message", "label": "Send a message", "icon": "mail"},
    {"id": "map", "label": "Map", "icon": "map-pin"},
]

TRANSPARENCY_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "budget", "label": "Budget", "icon": "landmark"},
    {"id": "procurement", "label": "Procurement", "icon": "file-text"},
    {"id": "plans", "label": "Plans", "icon": "compass"},
    {"id": "governance", "label": "Governance", "icon": "award"},
]

PRIVACY_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "collect", "label": "What we collect", "icon": "info"},
    {"id": "use", "label": "How we use it", "icon": "file-text"},
    {"id": "cookies", "label": "Cookies", "icon": "shield"},
    {"id": "rights", "label": "Your rights", "icon": "award"},
    {"id": "dpo", "label": "Contact", "icon": "mail"},
]

ACCESSIBILITY_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "features", "label": "Features", "icon": "shield"},
    {"id": "limitations", "label": "Limitations", "icon": "info"},
    {"id": "feedback", "label": "Feedback", "icon": "mail"},
]

SITEMAP_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "main", "label": "Main menu", "icon": "compass"},
    {"id": "pages", "label": "All pages", "icon": "file-text"},
]

FOI_SIDEBAR = [
    {"id": "page-top", "label": "Top", "icon": "home"},
    {"id": "about-foi", "label": "About FOI", "icon": "book"},
    {"id": "how", "label": "How to file", "icon": "info"},
    {"id": "exceptions", "label": "Exceptions", "icon": "shield"},
    {"id": "foi-contact", "label": "Contact", "icon": "mail"},
]

# ---------------------------------------------------------------------------
# About our city
# ---------------------------------------------------------------------------

CITY_PROFILE = {
    "lede": (
        "Puerto Princesa is the largest city in the Philippines by land area - "
        "2,381 square kilometres of coastline, forest, and limestone on the "
        "island of Palawan. It is the eco-tourism capital of the country and "
        "its first carbon neutral city."
    ),
    "intro": (
        "The city reaches from the Sulu Sea to the southern highlands, with 66 "
        "barangays, more than a hundred kilometres of shoreline, and one of the "
        "most intact tropical forests in the country. Tagbanua and Cuyonon "
        "traditions live alongside a modern city government serving around "
        "240,000 residents."
    ),
}

CITY_FACTS = [
    {"value": "66", "label": "Barangays across mainland and island communities"},
    {"value": "239,595", "label": "Residents at the 2020 census"},
    {"value": "2,381 km²", "label": "Total area - the largest city in the Philippines"},
    {"value": "1st", "label": "Carbon neutral city in the country"},
    {"value": "1999", "label": "UNESCO World Heritage Site designation"},
    {"value": "No. 1", "label": "Tourist destination in Palawan"},
]

HISTORY_POINTS = [
    {
        "period": "Early times",
        "title": "A homeland of the Tagbanua",
        "body": (
            "Long before the city charter, the Tagbanua of Cabayugan and the "
            "coast lived with the forest and the underground river. Their "
            "ancestral domain is still part of the city's identity today."
        ),
    },
    {
        "period": "1977",
        "title": "From town to city",
        "body": (
            "The settlement on the bay grew into a port town and was elevated "
            "to cityhood in 1977, opening a period of steady growth in trade, "
            "services, and population."
        ),
    },
    {
        "period": "1990s",
        "title": "A national model for the environment",
        "body": (
            "City reforms in the 1990s made the environment a governing "
            "priority - protected forests, cleaner streets, and a tourism "
            "policy built on conservation rather than extraction."
        ),
    },
    {
        "period": "1999 and 2012",
        "title": "A wonder of the world",
        "body": (
            "The Puerto Princesa Underground River was declared a UNESCO World "
            "Heritage Site in 1999 and named one of the New7Wonders of Nature "
            "in 2012, putting the city on the world map."
        ),
    },
]

# ---------------------------------------------------------------------------
# Government
# ---------------------------------------------------------------------------

GOVERNMENT_PILLARS = [
    {
        "name": "Vision and mission",
        "description": "Where the city is going, and how the government plans to get there.",
        "icon": "compass",
        "href": "https://puertoprincesa.ph/vision-mission/",
    },
    {
        "name": "Citizens' Charter",
        "description": "Every service, the office that delivers it, and how long it takes.",
        "icon": "file-text",
        "href": "https://puertoprincesa.ph/citizens-charter/",
    },
    {
        "name": "Performance pledge",
        "description": "The service standards the city commits to for every client.",
        "icon": "award",
        "href": "https://puertoprincesa.ph/performance-pledge/",
    },
    {
        "name": "Mayors and councilors",
        "description": "The elected officials of the city, past and present.",
        "icon": "users",
        "href": "https://puertoprincesa.ph/list-of-mayors-and-councilors/",
    },
    {
        "name": "City departments",
        "description": "The offices that run city services day to day.",
        "icon": "building",
        "href": "#departments",
    },
    {
        "name": "Full disclosure",
        "description": "Budgets, bids, and the documents behind every decision.",
        "icon": "landmark",
        "href": "https://puertoprincesa.ph/full-disclosure-government-transparency-new-v2/",
    },
]

DEPARTMENTS = [
    {"name": "Office of the City Mayor", "blurb": "Chief executive of the city government."},
    {"name": "Office of the City Vice Mayor", "blurb": "Presides over the Sangguniang Panlungsod."},
    {"name": "City Administrator's Office", "blurb": "Day-to-day administration of city affairs."},
    {"name": "City Planning and Development Office", "blurb": "Development plans, zoning, and land use."},
    {"name": "City Budget Office", "blurb": "Annual budget preparation and release."},
    {"name": "City Accounting Office", "blurb": "Accounts, payroll, and financial reporting."},
    {"name": "City Treasurer's Office", "blurb": "Tax collection and city revenues."},
    {"name": "City Assessor's Office", "blurb": "Property assessment and records."},
    {"name": "City Engineer's Office", "blurb": "Public works, roads, and infrastructure."},
    {"name": "Office of the City Building Official", "blurb": "Building and occupancy permits."},
    {"name": "City Health Office", "blurb": "Hospitals, health centers, and public health."},
    {"name": "City Social Welfare and Development Office", "blurb": "Assistance for families and vulnerable sectors."},
    {"name": "City Agriculturist's Office", "blurb": "Farming, fisheries, and food programs."},
    {"name": "City Tourism Office", "blurb": "Tourism promotion and visitor services."},
    {"name": "City Environment and Natural Resources Office", "blurb": "Clean air, water, forests, and waste."},
    {"name": "City Disaster Risk Reduction and Management Office", "blurb": "Preparedness, response, and rescue."},
    {"name": "City Public Employment Service Office", "blurb": "Job matching, training, and job fairs."},
    {"name": "City Information Office", "blurb": "Official news and public information."},
]

# ---------------------------------------------------------------------------
# Tourism
# ---------------------------------------------------------------------------

ATTRACTIONS = [
    {
        "name": "Puerto Princesa Underground River",
        "blurb": "A UNESCO World Heritage Site and one of the New7Wonders of Nature - 8.2 km of river winding through limestone caves.",
        "icon": "waves",
        "href": "https://undergroundriver.puertoprincesa.ph/",
    },
    {
        "name": "Honda Bay island hopping",
        "blurb": "A cluster of islands and sandbars a short boat ride from the city, known for snorkelling and clear shallows.",
        "icon": "map-pin",
        "href": "https://citytourism.puertoprincesa.ph/",
    },
    {
        "name": "Sabang mangrove forest",
        "blurb": "Paddle through one of the country's best-preserved mangrove forests, home to monitor lizards and birds.",
        "icon": "leaf",
        "href": "https://citytourism.puertoprincesa.ph/",
    },
    {
        "name": "Balayong People's Park",
        "blurb": "The city's green heart - blooming balayong trees, open lawns, and the festival grounds.",
        "icon": "award",
        "href": "https://puertoprincesa.ph/balayong-park/",
    },
    {
        "name": "Plaza Cuartel",
        "blurb": "A quiet memorial park in the city centre, marking a solemn chapter of the Second World War.",
        "icon": "landmark",
        "href": "https://citytourism.puertoprincesa.ph/",
    },
    {
        "name": "Baker's Hill",
        "blurb": "A hillside garden and bakery looking over the city, popular for afternoon walks and local pastries.",
        "icon": "building",
        "href": "https://citytourism.puertoprincesa.ph/",
    },
]

TRAVEL_TIPS = [
    {
        "question": "When is the best time to visit?",
        "answer": "The dry season runs from November to May. December to May is peak season, so book tours and rooms early.",
    },
    {
        "question": "How do I get to Puerto Princesa?",
        "answer": "Direct flights connect the Puerto Princesa International Airport with Manila, Cebu, and Clark. Buses and ferries link the city with other Palawan towns.",
    },
    {
        "question": "How do I book the Underground River?",
        "answer": "Daily visitor permits are limited. Book through the official Underground River site or an accredited tour operator before you travel.",
    },
    {
        "question": "How do I get around the city?",
        "answer": "Tricycles are the main way to move around the city centre. Vans and hired cars are best for day trips to Sabang and the bay.",
    },
    {
        "question": "What should I bring?",
        "answer": "Reef-safe sunscreen, a reusable water bottle, and light rain protection. Bring cash for small shops and tricycle fares.",
    },
]

# ---------------------------------------------------------------------------
# Directory (PROTOTYPE - only the City Hall switchboard is a real number;
# replace the rest with verified numbers before launch).
# ---------------------------------------------------------------------------

DIRECTORY_OFFICES = [
    {
        "name": "City Hall switchboard",
        "phone": "(048) 717-8000",
        "digits": "+63487178000",
        "email": "info@puertoprincesa.ph",
        "note": "Ask for the office you need. Mondays to Fridays, 8:00 AM to 5:00 PM.",
    },
    {
        "name": "City Disaster Risk Reduction and Management Office",
        "phone": "(048) 433-2470",
        "digits": "+63484332470",
        "email": "",
        "note": "Disaster response, rescue, and evacuation assistance.",
    },
    {
        "name": "City Health Office",
        "phone": "(048) 433-2158",
        "digits": "+63484332158",
        "email": "",
        "note": "Health programs, clinics, and medical assistance.",
    },
    {
        "name": "City Treasurer's Office",
        "phone": "(048) 433-2126",
        "digits": "+63484332126",
        "email": "",
        "note": "Real property tax and other city payments.",
    },
    {
        "name": "City Social Welfare and Development Office",
        "phone": "(048) 433-2188",
        "digits": "+63484332188",
        "email": "",
        "note": "Assistance for families, seniors, PWDs, and children.",
    },
    {
        "name": "City Tourism Office",
        "phone": "(048) 433-2062",
        "digits": "+63484332062",
        "email": "",
        "note": "Visitor information, tours, and accreditation.",
    },
    {
        "name": "City Public Employment Service Office",
        "phone": "(048) 433-2717",
        "digits": "+63484332717",
        "email": "",
        "note": "Job openings, job fairs, and livelihood training.",
    },
    {
        "name": "Office of the City Building Official",
        "phone": "(048) 433-2903",
        "digits": "+63484332903",
        "email": "",
        "note": "Building permits and occupancy certificates.",
    },
]

# ---------------------------------------------------------------------------
# Emergency page
# ---------------------------------------------------------------------------

SAFETY_TIPS = [
    {
        "title": "Before a typhoon",
        "body": "Monitor PAGASA bulletins, charge your phone and power banks, store drinking water, and prepare a go-bag with documents, medicine, and a flashlight.",
    },
    {
        "title": "During a flood",
        "body": "Move to higher ground early, avoid walking or driving through moving water, and switch off the main power if water reaches your home.",
    },
    {
        "title": "Fire",
        "body": "Stay low under smoke, get out and stay out, and call 911. Never use water on an electrical or grease fire.",
    },
    {
        "title": "At the beach or at sea",
        "body": "Check Coast Guard advisories before boat trips, keep children within arm's reach, and wear a life vest when riding small boats.",
    },
]

# ---------------------------------------------------------------------------
# Contact page
# ---------------------------------------------------------------------------

CONTACT_DETAILS = {
    "address": "City Hall, Rizal Avenue, Puerto Princesa City, 5300 Palawan, Philippines",
    "phone": "(048) 717-8000",
    "phone_digits": "+63 48 717 8000",
    "email": "info@puertoprincesa.ph",
    "hours": "Mondays to Fridays, 8:00 AM to 5:00 PM (except regular holidays)",
    "facebook": "https://www.facebook.com/puertoprincesaph",
    "map_url": "https://maps.app.goo.gl/9UqPadrmTNHS72XR8",
    "map_embed": (
        "https://maps.google.com/maps?q=Puerto+Princesa+City+Hall"
        "&z=14&output=embed"
    ),
}

CONTACT_TOPICS = [
    "General inquiry",
    "Complaint or feedback",
    "Request for assistance",
    "Business permits and licensing",
    "Tourism and travel",
    "Employment and careers",
    "Other",
]

CONTACT_FAQS = [
    {
        "question": "How soon will I get a reply?",
        "answer": (
            "Messages are routed to the responsible office and acknowledged within "
            "three working days. Complex requests may take longer, but you will be "
            "told which office is handling it."
        ),
    },
    {
        "question": "Where do I follow up a service request?",
        "answer": (
            "Where a request is covered by the Citizens' Charter, you will be given a "
            "reference number and the name of the officer to follow up with."
        ),
    },
    {
        "question": "I need help right now.",
        "answer": (
            "This form is not monitored around the clock. For emergencies call 911 or "
            "open the emergency panel at the bottom-right of any page for direct lines."
        ),
    },
]

# ---------------------------------------------------------------------------
# Transparency (Full Disclosure Policy). Links point to the live site's public
# documents until the prototype is wired to a document store.
# ---------------------------------------------------------------------------

_FULL_DISCLOSURE = "https://puertoprincesa.ph/full-disclosure-government-transparency-new-v2/"

TRANSPARENCY_GROUPS = [
    {
        "name": "Budget and finance",
        "id": "budget",
        "icon": "landmark",
        "blurb": "How the city raises and spends public money.",
        "items": [
            {"name": "Annual budget", "note": "The budget approved by the City Council for the current fiscal year.", "href": _FULL_DISCLOSURE},
            {"name": "Statement of receipts and expenditures", "note": "Actual income and spending against the approved budget.", "href": _FULL_DISCLOSURE},
            {"name": "Budget execution documents", "note": "Quarterly reports on how the budget is being used.", "href": _FULL_DISCLOSURE},
        ],
    },
    {
        "name": "Procurement",
        "id": "procurement",
        "icon": "file-text",
        "blurb": "What the city is buying, and who it awarded the contract to.",
        "items": [
            {"name": "Annual procurement plan", "note": "Goods, works, and services the city plans to procure.", "href": _FULL_DISCLOSURE},
            {"name": "Bids and awards", "note": "Bid notices and results from the Bids and Awards Committee.", "href": "https://bacoffice.puertoprincesa.ph/"},
            {"name": "Awarded contracts", "note": "Contracts awarded and their corresponding amounts.", "href": _FULL_DISCLOSURE},
        ],
    },
    {
        "name": "Plans and reports",
        "id": "plans",
        "icon": "compass",
        "blurb": "The plans that guide the city's development.",
        "items": [
            {"name": "Comprehensive development plan", "note": "The city's multi-year development direction.", "href": _FULL_DISCLOSURE},
            {"name": "Annual investment program", "note": "Programs and projects funded for the year.", "href": _FULL_DISCLOSURE},
            {"name": "Executive-legislative agenda", "note": "Shared priorities of the mayor and the City Council.", "href": _FULL_DISCLOSURE},
        ],
    },
    {
        "name": "Governance",
        "id": "governance",
        "icon": "award",
        "blurb": "Service standards, officials' disclosures, and performance.",
        "items": [
            {"name": "Citizens' Charter", "note": "Step-by-step service standards for every frontline office.", "href": "https://puertoprincesa.ph/citizens-charter/"},
            {"name": "Performance pledge", "note": "The service commitments the city holds itself to.", "href": "https://puertoprincesa.ph/performance-pledge/"},
            {"name": "SALN and financial disclosures", "note": "Statements of assets, liabilities, and net worth of officials.", "href": _FULL_DISCLOSURE},
        ],
    },
]

# ---------------------------------------------------------------------------
# Privacy policy
# ---------------------------------------------------------------------------

PRIVACY_SECTIONS = [
    {
        "id": "collect",
        "title": "What we collect",
        "paragraphs": [
            "We collect information you give us directly, such as your name, contact details, and the content of a message sent through a form on this site or by email.",
            "When you browse this site, our servers record technical information such as your IP address, browser type, the pages you visit, and the time of your visit, used in aggregate to keep the site secure and working.",
        ],
    },
    {
        "id": "use",
        "title": "How we use your information",
        "paragraphs": [
            "Information you send is used only to respond to your request, deliver the service you asked for, and keep a record of the transaction.",
            "We do not sell personal information. We share it with another office only when that office is the one that can act on your request, and only to the extent needed.",
        ],
    },
    {
        "id": "cookies",
        "title": "Cookies and analytics",
        "paragraphs": [
            "This site uses a small number of essential cookies to remember form progress and to keep sessions secure. These cookies do not identify you personally.",
            "If analytics are enabled, they are configured to report only aggregated, non-identifying statistics. You can block or delete cookies in your browser settings without losing access to any content on this site.",
        ],
    },
    {
        "id": "rights",
        "title": "Your rights under the Data Privacy Act",
        "paragraphs": [
            "Under Republic Act No. 10173, the Data Privacy Act of 2012, you have the right to be informed, to object, to access, to correct, to erase or block, to damages, to file a complaint, and to data portability.",
            "To exercise any of these rights, write to the city's Data Protection Officer using the contact details below. Requests are acted on within the period set by the National Privacy Commission.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Accessibility statement
# ---------------------------------------------------------------------------

ACCESSIBILITY_FEATURES = [
    "Text and interface colours meet the WCAG 2.1 AA contrast minimum.",
    "Every page can be used with a keyboard alone, including the side navigation.",
    "Interactive parts expose their state to screen readers with ARIA attributes.",
    "Animations respect the operating system's reduced-motion setting.",
    "Images carry descriptive alternative text; decorative images are ignored.",
    "Pages are built with real headings and landmarks, so structure is announced.",
    "Tap targets on phones are at least 44 by 44 pixels.",
    "The site works without JavaScript, with a plain fallback for every widget.",
]

ACCESSIBILITY_SECTIONS = [
    {
        "id": "commitment",
        "title": "Our commitment",
        "paragraphs": [
            "The City Government of Puerto Princesa wants every resident to be able to use this site, including people who use screen readers, keyboard navigation, screen magnifiers, or who are deaf or hard of hearing.",
            "We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at Level AA, and we follow Republic Act No. 7277, the Magna Carta for Persons with Disability, as amended.",
        ],
    },
    {
        "id": "limitations",
        "title": "Known limitations",
        "paragraphs": [
            "Some older documents published as scanned images cannot yet be read by screen readers. We are re-publishing the most requested ones as tagged PDFs.",
            "Third-party portals linked from this site, such as the national eFOI and eGov services, are outside our control and may not meet the same standard.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Freedom of Information
# ---------------------------------------------------------------------------

FOI_REQUESTS = [
    "City ordinances, resolutions, and minutes of the Sangguniang Panlungsod",
    "Budgets, financial reports, and statements of receipts and expenditures",
    "Contracts, purchase orders, and procurement records",
    "Development plans, zoning records, and permits",
    "Program and project documents, including progress reports",
]

FOI_STEPS = [
    {
        "title": "File your request",
        "body": "File through the national eFOI portal at foi.gov.ph, or submit a written request to the city's FOI Receiving Officer at City Hall. Include your name, contact details, and a clear description of the records you need.",
    },
    {
        "title": "We acknowledge",
        "body": "The receiving officer logs your request and confirms within a few days whether the records exist and which office holds them.",
    },
    {
        "title": "We respond",
        "body": "You receive the records, or a written reason for refusal, within 15 working days. This may be extended once by another 15 working days, with notice to you.",
    },
    {
        "title": "If you are refused",
        "body": "A refusal states the legal ground and your right to appeal. You may ask for a review by the city's appeals authority, and ultimately by the National Privacy Commission or the courts, depending on the ground.",
    },
]

FOI_EXCEPTIONS = [
    "Information covered by a lawful privilege or affecting national security",
    "Information that would prejudice an ongoing investigation or law enforcement",
    "Personal information protected under the Data Privacy Act",
    "Records that are already published and publicly available",
]
