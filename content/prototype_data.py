"""PROTOTYPE ONLY - fake/curated content for design review on the `prototype` branch.

Content is based on the real city website (https://puertoprincesa.ph/) so the
redesign can be reviewed with realistic material: real headlines, real service
links, real festivals. Dates for news are fixed (taken from the live site);
event dates are computed from today so nothing ever looks expired.

When the redesign is approved, replace the context in content.views.home with
Article/Event/Notice/Service queries and delete this file.

External links (marked below) point at the live city site and partner portals.
"""

from datetime import date, timedelta

from .news_data import NEWS_ARTICLES

# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

TAGLINE = (
    "The City Nestled Within the Heart of the Forest, Where Nature and Progress Thrive in Harmony."
)

FACEBOOK_URL = "https://www.facebook.com/puertoprincesaph"

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
    {
        "stat": "8.2 km",
        "label": "Total length of the underground river",
        "value": 8.2,
        "suffix": " km",
    },
    {"stat": "4.3 km", "label": "Navigable section of the river", "value": 4.3, "suffix": " km"},
    {"stat": "1 of 7", "label": "New7Wonders of Nature", "value": None, "suffix": ""},
    {"stat": "1999", "label": "UNESCO Heritage Site designation", "value": 1999, "suffix": ""},
    {"stat": "100+", "label": "Unique wildlife species", "value": 100, "suffix": "+"},
    {
        "stat": "20M+ years",
        "label": "Age of limestone formations",
        "value": 20,
        "suffix": "M+ years",
    },
]

# ---------------------------------------------------------------------------
# Emergency quick-dial.
# Source: puertoprincesa.ph/city-emergency-contacts/ (verified November 2026).
# Where the city publishes both a short code and a landline, the landline is
# the tap-to-call number and the short code is named in the note.
# ---------------------------------------------------------------------------

EMERGENCY_CONTACTS = [
    {
        "name": "National Emergency Hotline",
        "number": "911",
        "digits": "911",
        "note": "Police, fire, ambulance, and rescue - nationwide",
    },
    {
        "name": "Puerto Princesa City Police Station",
        "number": "(048) 434-9890",
        "digits": "+63484349890",
        "note": "Police assistance. National police hotline: 166. Alternate line: (048) 434-9889.",
    },
    {
        "name": "Bureau of Fire Protection",
        "number": "(048) 434-2076",
        "digits": "+63484342076",
        "note": "Fire and rescue response. National fire hotline: 160.",
    },
    {
        "name": "Palawan Provincial Hospital",
        "number": "(048) 433-2621",
        "digits": "+63484332621",
        "note": "Public hospital emergency room. Provincial hospital hotline: 169.",
    },
    {
        "name": "City Health Office hotline",
        "number": "(048) 434-6582",
        "digits": "+63484346582",
        "note": "Medical assistance and city health services. Main line: (048) 717-8084.",
    },
    {
        "name": "Philippine Red Cross - Palawan",
        "number": "(048) 433-6362",
        "digits": "+63484336362",
        "note": "Emergency assistance, ambulance, and first aid.",
    },
    {
        "name": "PAGASA Puerto Princesa",
        "number": "(048) 433-5192",
        "digits": "+63484335192",
        "note": "Weather forecasts and typhoon bulletins.",
    },
    {
        "name": "City Government switchboard",
        "number": "(048) 717-8000",
        "digits": "+63487178000",
        "note": "City Hall - ask for the office or service you need.",
    },
]

# ---------------------------------------------------------------------------
# Mayor's Corner (profile from the live site)
# ---------------------------------------------------------------------------

MAYOR = {
    "name": "Hon. Lucilo R. Bayron",
    "title": "City Mayor",
    "photo": "img/mayor-bayron.png",
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
        "title": "Water service interruption in selected barangays",
        "body": (
            "Emergency repair work on a transmission line will interrupt water service "
            "in Barangays San Pedro, San Jose, and Tiniguiban from 9:00 AM to 3:00 PM. "
            "Residents are advised to store water ahead of the interruption."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "City Assessor's Office services, now closer to residents",
        "body": (
            "Property assessment records and certification services are now available at "
            "the mini-City Hall in Barangay San Pedro every weekday from 8:00 AM to 5:00 PM."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Puerto Princesa City Mental Health and Wellness Clinic, open to the public",
        "body": (
            "Free counseling and mental health consultations are available at the City "
            "Health Office annex. Walk-ins are welcome from Monday to Friday."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Sunburn: do not underestimate it - it is serious skin damage too",
        "body": (
            "The City Health Office reminds residents to use sunscreen, wear protective "
            "clothing, and avoid prolonged sun exposure, especially between 10:00 AM and 4:00 PM."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Barangay clearance processing schedule for December",
        "body": (
            "Barangay clearance desks will extend their hours to 6:00 PM on weekdays until "
            "December 20 to accommodate residents renewing permits and clearances."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Road reblocking along Rizal Avenue this weekend",
        "body": (
            "A section of Rizal Avenue near the public market will be closed from 10:00 PM "
            "on Saturday to 5:00 AM on Sunday for drainage and asphalt repair. Use alternate routes."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Free anti-rabies vaccination for pets",
        "body": (
            "The City Veterinary Office will hold free anti-rabies vaccination in Barangays "
            "Manggahan, Sicsican, and Irawan. Bring pets in secure carriers or on a leash."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "City scholarship applications now open",
        "body": (
            "Qualified senior high school and college students may submit scholarship "
            "applications at the City Social Welfare and Development Office until the end of the month."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Senior citizen ID renewal schedule",
        "body": (
            "Senior citizens may renew their IDs at the Office of the Senior Citizens Affairs "
            "from Monday to Friday. Bring a valid ID and a recent 1x1 photo."
        ),
        "href": "https://puertoprincesa.ph/notices-and-announcements/",
    },
    {
        "title": "Holiday garbage collection schedule",
        "body": (
            "Garbage collection will follow a adjusted schedule during the holiday period. "
            "Residents are asked to segregate waste and place bins outside after 5:00 PM."
        ),
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
        "description": "A family-friendly morning of fishing, games, and prizes at the city's newest park.",
        "href": "https://puertoprincesa.ph/events/fun-fishing-day/",
    },
    {
        "title": "The Philippine Beach Games Puerto Princesa media launch",
        "date": _ahead(15),
        "time": "4:00 PM",
        "venue": "The Dome Hotel, Puerto Princesa",
        "description": "The city and its partners launch the Philippine Beach Games with athletes, coaches, and media.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Blessing and inauguration of the Screaming Eagle Zipline",
        "date": _ahead(22),
        "time": "8:00 AM",
        "venue": "Balayong People's Park",
        "description": "The city opens a new zipline attraction at Balayong People's Park.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "City-wide coastal clean-up",
        "date": _ahead(29),
        "time": "6:30 AM",
        "venue": "City Baywalk and Sabang Beach",
        "description": "Volunteers, schools, and barangays clean up the city's shoreline and mangrove areas.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Barangay health caravan",
        "date": _ahead(36),
        "time": "8:00 AM",
        "venue": "Barangay Irawan covered court",
        "description": "Free check-ups, medicines, and health consultations for residents.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Pista y ang Cagueban tree planting",
        "date": _ahead(43),
        "time": "7:00 AM",
        "venue": "Irawan watershed",
        "description": "The city's annual forest festival brings residents together to plant native trees.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Youth sports festival",
        "date": _ahead(50),
        "time": "8:00 AM",
        "venue": "RVM Sports Complex",
        "description": "Basketball, volleyball, and athletics competitions for city youth.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Business permit renewal clinic",
        "date": _ahead(57),
        "time": "9:00 AM",
        "venue": "City Coliseum",
        "description": "One-stop assistance for business permit renewal and tax payments.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Cultural night at Plaza Cuartel",
        "date": _ahead(64),
        "time": "6:00 PM",
        "venue": "Plaza Cuartel",
        "description": "An evening of music, dance, and local food celebrating Puerto Princesa's heritage.",
        "href": "https://puertoprincesa.ph/events/",
    },
    {
        "title": "Subaraw Biodiversity Festival 2027 kick-off",
        "date": _ahead(71),
        "time": "5:00 PM",
        "venue": "Edward S. Hagedorn Coliseum",
        "description": "The city begins preparations for next year's Subaraw festival with partners and stakeholders.",
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
# Sources for the July-December entries: the official Puerto Princesa Tourism
# calendar (puertoprincesatourism.com/calendar) and the city government's
# Festival and Special Events pages (puertoprincesa.ph). Every entry is held
# inside Puerto Princesa City itself.
FESTIVALS = [
    {
        "month": "Jan",
        "when": "1",
        "name": "Bagong Taon Bagong Buhay sa Baybay",
        "blurb": "New Year celebration at the City Baywalk",
    },
    {
        "month": "Feb",
        "when": "14",
        "name": "Love Affair with Nature",
        "blurb": "Mangrove planting and nature activities",
    },
    {
        "month": "Mar",
        "when": "4",
        "name": "Balayong Festival",
        "blurb": "Citywide celebration of the Palawan cherry",
    },
    {
        "month": "Apr",
        "when": "Week 1",
        "name": "Pangalipay sa Baybay",
        "blurb": "Week of coastal festivities after the fiesta",
    },
    {
        "month": "May",
        "when": "1",
        "name": "Karagatan Festival",
        "blurb": "Month of the Ocean celebration",
    },
    {
        "month": "Jun",
        "when": "4th Sat",
        "name": "Pista y ang Cagueban",
        "blurb": "Forest festival and tree planting for the youth",
    },
    {
        "month": "Jul",
        "when": "Month-long",
        "name": "Sports Fair",
        "blurb": "Basketball, swimming, motocross and other meets in the Sports Capital of the Philippines",
    },
    {
        "month": "Aug",
        "when": "Month-long",
        "name": "Eco-Tourism Adventure",
        "blurb": "Guided outdoor adventures around the city's forests, rivers and bays, running into September",
    },
    {
        "month": "Sep",
        "when": "Month-long",
        "name": "Tandikan Festival",
        "blurb": "Tourism month showcase of performances, local cuisine and tourism services",
    },
    {
        "month": "Oct",
        "when": "Week 4",
        "name": "Kalag-kalag Festival",
        "blurb": "The city's Halloween season - zombie run, horror dance and costume contests",
    },
    {
        "month": "Nov",
        "when": "Week 1",
        "name": "Subaraw Biodiversity Festival",
        "blurb": "Week-long celebration of the city's biodiversity, timed to the Underground River's New 7 Wonders anniversary",
    },
    {
        "month": "Dec",
        "when": "1",
        "name": "Pista Na, Pasko Pa",
        "blurb": "Giant Christmas tree lighting kicks off a month of nightly shows",
    },
    {
        "month": "Dec",
        "when": "8",
        "name": "City Fiesta",
        "blurb": "Feast of the Immaculate Conception, the city's patroness, with processions and community celebrations",
    },
]

# ---------------------------------------------------------------------------
# Honors and seals (local copies of the live site's images; see photo_credits)
# ---------------------------------------------------------------------------

SEALS = [
    (
        "img/seals/city-government-seal.png",
        "City Government seal",
    ),
    (
        "img/seals/underground-river-mark.png",
        "Puerto Princesa Underground River brand mark",
    ),
    ("img/seals/iso-certification.png", "ISO certification mark"),
    ("img/seals/award-seal-1.png", "Award seal"),
    ("img/seals/award-seal-2.png", "Award seal"),
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
    {"id": "gallery", "label": "In photos", "icon": "map-pin"},
    {"id": "history", "label": "History", "icon": "book"},
    {"id": "culture", "label": "Culture", "icon": "users"},
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
    {"id": "retention", "label": "Retention", "icon": "clock"},
    {"id": "third-parties", "label": "Third parties", "icon": "users"},
    {"id": "cookies", "label": "Cookies", "icon": "shield"},
    {"id": "security", "label": "Security", "icon": "shield"},
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
        "The city government describes Puerto Princesa as the largest city in "
        "the Philippines by land area: 253,982 hectares of coastline, forest, "
        "and limestone on the island of Palawan. It is the eco-tourism capital "
        "of the country and its first carbon neutral city."
    ),
    "intro": (
        "The city stretches 106 kilometres from north to south, from the Sulu "
        "Sea to the southern highlands, with 66 barangays - 35 urban and 31 "
        "rural - and one of the most intact tropical forests in the country. "
        "Tagbanua and Cuyonon traditions live alongside a modern city "
        "government serving a growing population."
    ),
}

# Figures below follow the city government's own published pages. Where the
# official site conflicts with itself (for example, its key-facts and history
# pages give different population counts), the figure is left out rather than
# presenting a number the city does not consistently publish.
CITY_FACTS = [
    {
        "value": "66",
        "label": "Barangays, made up of 35 urban and 31 rural",
        "source": "City Government of Puerto Princesa, Geography",
    },
    {
        "value": "253,982 ha",
        "label": "Land area, described by the city as the country's largest",
        "source": "City Government of Puerto Princesa, Geography",
    },
    {
        "value": "8.5 km",
        "label": "Narrowest breadth, at Bahile",
        "source": "City Government of Puerto Princesa, Key Facts",
    },
    {
        "value": "1970",
        "label": "Year Puerto Princesa became a city",
        "source": "City Government of Puerto Princesa, History",
    },
    {
        "value": "1st",
        "label": "Carbon neutral city in the country",
        "source": "City Government of Puerto Princesa, About our city",
    },
    {
        "value": "1999",
        "label": "UNESCO World Heritage Site designation",
        "source": "UNESCO World Heritage List",
    },
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
        "period": "1970",
        "title": "From town to city",
        "body": (
            "The settlement on the bay grew into a port town and became a city "
            "in 1970, opening a period of steady growth in trade, services, and "
            "population."
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

# Small chips under the city profile intro. Each one points back to a fact
# above, so the page reads as a story before it becomes a table of figures.
# Barangay breakdown, as published on the city government's Geography page.
CITY_BARANGAYS = {
    "total": 66,
    "urban": 35,
    "rural": 31,
    "urban_area": "14,716",
    "rural_area": "239,266",
    "urban_share": "5.79",
    "rural_share": "94.21",
    "source": "City Government of Puerto Princesa, Geography",
}

CITY_PROFILE_HIGHLIGHTS = [
    {"label": "253,982 hectares of land", "icon": "map-pin"},
    {"label": "UNESCO World Heritage site", "icon": "award"},
    {"label": "First carbon-neutral city", "icon": "leaf"},
    {"label": "66 barangays", "icon": "users"},
]

# Access strip: how a visitor reaches the city and its best-known site. Times
# are typical, not timetabled, so the copy stays honest.
CITY_JOURNEYS = [
    {
        "title": "Fly in",
        "body": "Direct flights from Manila take about an hour and twenty minutes. The airport is a short ride from the baywalk.",
        "icon": "compass",
    },
    {
        "title": "Ride to Sabang",
        "body": "Vans and buses follow the coastal road roughly 80 kilometres north to Sabang in about two hours.",
        "icon": "map-pin",
    },
    {
        "title": "Boat to the cave",
        "body": "Outrigger boats cross from Sabang to the Underground River entrance in about twenty minutes, weather permitting.",
        "icon": "waves",
    },
    {
        "title": "Move around town",
        "body": "Tricycles and jeepneys link the baywalk, public market, plazas, and the New City Hall in Sta. Monica Heights.",
        "icon": "landmark",
    },
]

# Three short culture cards for the closing section. Photos come from the same
# local CITY_PHOTOS library and are credited on the photo credits page.
CITY_CULTURE = [
    {
        "title": "Tagbanua heritage",
        "body": (
            "The Tagbanua of Cabayugan and the southern highlands are the "
            "city's first stewards. Their ancestral domain, language, and "
            "forest knowledge remain part of how Puerto Princesa sees itself."
        ),
        "image": "city-limestone",
        "alt": "Limestone karst formations in the Puerto Princesa Subterranean River National Park",
        "icon": "leaf",
    },
    {
        "title": "Life on the coast",
        "body": (
            "Fishing villages, island barangays, and the baywalk all turn "
            "toward the Sulu Sea. Boats, markets, and the evening promenade "
            "are still the rhythm of the city."
        ),
        "image": "city-sabang",
        "alt": "The long grey-sand shoreline of Sabang Beach in Puerto Princesa",
        "icon": "waves",
    },
    {
        "title": "Faith and festivals",
        "body": (
            "Church calendars and city fiestas fill the plaza year-round, from "
            "the Feast of the Immaculate Conception to the festivals that "
            "celebrate the city's founding."
        ),
        "image": "city-cathedral",
        "alt": "The blue-and-white facade of the Immaculate Conception Cathedral",
        "icon": "star",
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
    {
        "name": "City Planning and Development Office",
        "blurb": "Development plans, zoning, and land use.",
    },
    {"name": "City Budget Office", "blurb": "Annual budget preparation and release."},
    {"name": "City Accounting Office", "blurb": "Accounts, payroll, and financial reporting."},
    {"name": "City Treasurer's Office", "blurb": "Tax collection and city revenues."},
    {"name": "City Assessor's Office", "blurb": "Property assessment and records."},
    {"name": "City Engineer's Office", "blurb": "Public works, roads, and infrastructure."},
    {"name": "Office of the City Building Official", "blurb": "Building and occupancy permits."},
    {"name": "City Health Office", "blurb": "Hospitals, health centers, and public health."},
    {
        "name": "City Social Welfare and Development Office",
        "blurb": "Assistance for families and vulnerable sectors.",
    },
    {"name": "City Agriculturist's Office", "blurb": "Farming, fisheries, and food programs."},
    {"name": "City Tourism Office", "blurb": "Tourism promotion and visitor services."},
    {
        "name": "City Environment and Natural Resources Office",
        "blurb": "Clean air, water, forests, and waste.",
    },
    {
        "name": "City Disaster Risk Reduction and Management Office",
        "blurb": "Preparedness, response, and rescue.",
    },
    {
        "name": "City Public Employment Service Office",
        "blurb": "Job matching, training, and job fairs.",
    },
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
        "image": "spot-underground",
        "alt": "A tour boat inside the Cathedral Chamber of the Puerto Princesa Underground River",
        "credit": "lumoplank / CC0",
    },
    {
        "name": "Honda Bay island hopping",
        "blurb": "A cluster of islands and sandbars a short boat ride from the city, known for snorkelling and clear shallows.",
        "icon": "map-pin",
        "href": "https://citytourism.puertoprincesa.ph/",
        "image": "spot-honda",
        "alt": "Clear turquoise water and a sandbar at Luli Island in Honda Bay",
        "credit": "mendhak / CC BY-SA 2.0",
    },
    {
        "name": "Sabang mangrove forest",
        "blurb": "Paddle through one of the country's best-preserved mangrove forests, home to monitor lizards and birds.",
        "icon": "leaf",
        "href": "https://citytourism.puertoprincesa.ph/",
        "image": "spot-sabang",
        "alt": "The long grey-sand shoreline of Sabang Beach in Puerto Princesa",
        "credit": "Patrickroque01 / CC BY-SA 4.0",
    },
    {
        "name": "Puerto Princesa City Baywalk",
        "blurb": "The city's waterfront promenade - sunrise views over the bay, food stalls, and a breezy walk after dark.",
        "icon": "award",
        "href": "https://puertoprincesa.ph/",
        "image": "spot-baywalk",
        "alt": "The Puerto Princesa City Baywalk and its waterfront on a clear day",
        "credit": "Patrickroque01 / CC BY-SA 4.0",
    },
    {
        "name": "Plaza Cuartel",
        "blurb": "A quiet memorial park in the city centre, marking a solemn chapter of the Second World War.",
        "icon": "landmark",
        "href": "https://citytourism.puertoprincesa.ph/",
        "image": "spot-plaza",
        "alt": "The stone gate and grounds of Plaza Cuartel in Puerto Princesa",
        "credit": "Patrickroque01 / CC BY-SA 4.0",
    },
    {
        "name": "Baker's Hill",
        "blurb": "A hillside garden and bakery looking over the city, popular for afternoon walks and local pastries.",
        "icon": "building",
        "href": "https://citytourism.puertoprincesa.ph/",
        "image": "spot-bakers",
        "alt": "A view over the grounds and hills from Baker's Hill in Puerto Princesa",
        "credit": "shankar s. / CC BY 2.0",
    },
]

# ---------------------------------------------------------------------------
# City in photos (homepage strip). Photos are local copies of Wikimedia
# Commons files; the visible credit line keeps the licence attribution intact.
# ---------------------------------------------------------------------------

CITY_PHOTOS = [
    {
        "image": "city-baywalk",
        "alt": "The Puerto Princesa City Baywalk and waterfront on a clear day",
        "caption": "City Baywalk",
        "credit": "Patrickroque01",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_City_Baywalk_(Puerto_Princesa,_Palawan;_08-03-2023).jpg",
    },
    {
        "image": "city-underground",
        "alt": "A tour boat inside the Cathedral Chamber of the Puerto Princesa Underground River",
        "caption": "Underground River",
        "credit": "lumoplank",
        "license": "CC0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_Subterranean_River_-_PuertoPrincesaSR1755.jpg",
    },
    {
        "image": "city-sabang",
        "alt": "The long grey-sand shoreline of Sabang Beach in Puerto Princesa",
        "caption": "Sabang Beach",
        "credit": "Patrickroque01",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Sabang_Beach_front_west_(Cabayugan,_Puerto_Princesa,_Palawan;_08-04-2023).jpg",
    },
    {
        "image": "city-cathedral",
        "alt": "The blue-and-white facade of the Immaculate Conception Cathedral",
        "caption": "Immaculate Conception Cathedral",
        "credit": "Herbertkikoy",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Immaculate_Conception_Cathedral_-_Puerto_Princesa_City.jpg",
    },
    {
        "image": "city-iwahig",
        "alt": "The Iwahig River flowing through green forest in Puerto Princesa",
        "caption": "Iwahig River",
        "credit": "Filipinayzd",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Iwahig_River,_Puerto_Princesa_City.jpg",
    },
    {
        "image": "city-limestone",
        "alt": "Limestone karst formations in the Puerto Princesa Subterranean River National Park",
        "caption": "Subterranean River National Park",
        "credit": "Vyacheslav Argenberg",
        "license": "CC BY 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_Subterranean_Park,_limestone_formations,_Palawan,_Philippines.jpg",
    },
]

# Hero banner slideshow. Three stills from the city government's own Balayong
# People's Park banner video cross-fade behind the blue-to-dark overlay. Using
# stills keeps the look of the live hero without the weight of the full video.
# Photos are credited on the photo credits page.
HERO_SLIDES = [
    {
        "image": "hero-balayong-1",
        "alt": "",
        "caption": "Balayong People's Park",
        "credit": "City Government of Puerto Princesa",
        "license": "Official city video still",
        "source": "https://puertoprincesa.ph/",
    },
    {
        "image": "hero-balayong-2",
        "alt": "",
        "caption": "Aerial view of Puerto Princesa",
        "credit": "City Government of Puerto Princesa",
        "license": "Official city video still",
        "source": "https://puertoprincesa.ph/",
    },
    {
        "image": "hero-balayong-3",
        "alt": "",
        "caption": "The city and its coastline",
        "credit": "City Government of Puerto Princesa",
        "license": "Official city video still",
        "source": "https://puertoprincesa.ph/",
    },
]

# Every local photo used on the public site. Attribution lives on one credits
# page (linked from the footer) so content pages stay clean while the licence
# terms remain easy to find.
PHOTO_CREDITS = [
    {
        "title": "Balayong People's Park hero stills",
        "author": "City Government of Puerto Princesa",
        "license": "Official city video still",
        "source": "https://puertoprincesa.ph/",
    },
    {
        "title": "Sunrise over the City Baywalk",
        "author": "Iamsandraguia",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:PPC_Baywalk_Sunrise.jpg",
    },
    {
        "title": "Puerto Princesa Subterranean River",
        "author": "lumoplank",
        "license": "CC0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_Subterranean_River_-_PuertoPrincesaSR1755.jpg",
    },
    {
        "title": "Limestone formations, Subterranean River National Park",
        "author": "Vyacheslav Argenberg",
        "license": "CC BY 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_Subterranean_Park,_limestone_formations,_Palawan,_Philippines.jpg",
    },
    {
        "title": "Puerto Princesa City Baywalk",
        "author": "Patrickroque01",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_City_Baywalk_(Puerto_Princesa,_Palawan;_08-03-2023).jpg",
    },
    {
        "title": "Immaculate Conception Cathedral",
        "author": "Herbertkikoy",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Immaculate_Conception_Cathedral_-_Puerto_Princesa_City.jpg",
    },
    {
        "title": "Iwahig River",
        "author": "Filipinayzd",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Iwahig_River,_Puerto_Princesa_City.jpg",
    },
    {
        "title": "Sabang Beach",
        "author": "Patrickroque01",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Sabang_Beach_front_west_(Cabayugan,_Puerto_Princesa,_Palawan;_08-04-2023).jpg",
    },
    {
        "title": "Puerto Princesa International Airport",
        "author": "Luisztdt",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Puerto_Princesa_International_Airport_Outside_1.jpg",
    },
    {
        "title": "Luli Island, Honda Bay",
        "author": "mendhak",
        "license": "CC BY-SA 2.0",
        "source": "https://commons.wikimedia.org/wiki/File:Luli_Island,_Honda_Bay,_Palawan,_Philippines.jpg",
    },
    {
        "title": "Plaza Cuartel",
        "author": "Patrickroque01",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Plaza_Cuartel_(Taft_Street,_Puerto_Princesa,_Palawan;_08-03-2023).jpg",
    },
    {
        "title": "View from Baker's Hill",
        "author": "shankar s.",
        "license": "CC BY 2.0",
        "source": "https://commons.wikimedia.org/wiki/File:View_from_Baker%27s_Hill_(9162925937).jpg",
    },
    {
        "title": "Fun Fishing Day at Balayong People's Park",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/events/fun-fishing-day/",
    },
    {
        "title": "Philippine Beach Games Puerto Princesa media launch",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/events/the-philippine-beach-games-puerto-princesa-media-launch-at-the-dome-hotel-puerto-princesa/",
    },
    {
        "title": "Screaming Eagle Zipline at Balayong People's Park",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/events/the-blessing-and-inauguration-of-screaming-eagle-zipline-at-balayong-peoples-park/",
    },
    {
        "title": "Subaraw Festival Queen 2026",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/902045018_1541760017771973_680363610239350466_n.jpg",
    },
    {
        "title": "Subaraw Biodiversity Festival 2026 closing program",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/904356981_987133897275308_3415584307256719428_n.jpg",
    },
    {
        "title": "Subaraw National Hiphop Dance Competition 2026",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/896102613_1976723640380228_4927144652985755348_n.jpg",
    },
    {
        "title": "City Peso bread-making training",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/BALITANG-CIO-5.png",
    },
    {
        "title": "Subaraw drum and lyre competition",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/897938011_990874213480412_4697660152567565617_n.jpg",
    },
    {
        "title": "Subaraw National Music Championship announcement",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/900352850_1147815527709162_5573125317308333185_n.jpg",
    },
    {
        "title": "Subaraw Festival 2026 program at SM City",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/897438800_1841310437058676_8392580907051454230_n.jpg",
    },
    {
        "title": "Tagburos Elementary School stage inauguration",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/897387491_2644212412693036_8476217773788611719_n.jpg",
    },
    {
        "title": "Subaraw Biodiversity Festival 2026 grand opening",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/892009628_1655918335916101_4584292344636021980_n.jpg",
    },
    {
        "title": "Subaraw 2026 opening in Sitio Sabang",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/891289952_2412797842854049_7898559470865284561_n.jpg",
    },
    {
        "title": "BFP Puerto Princesa courtesy call",
        "author": "City Government of Puerto Princesa",
        "license": "Official city photo",
        "source": "https://puertoprincesa.ph/wp-content/uploads/2026/11/886896212_1784080262871846_803042454875920870_n.jpg",
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
# ---------------------------------------------------------------------------
# Directory.
# Source: puertoprincesa.ph/city-government-contacts/ (verified November 2026).
# The city publishes a single mailbox (info@puertoprincesa.ph) for general
# inquiries, so offices without a published address are listed by phone only.
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
        "name": "Business Permits and Licensing Office",
        "phone": "(048) 717-8008",
        "digits": "+63487178008",
        "email": "",
        "note": "New and renewing business permits, and licensing inquiries.",
    },
    {
        "name": "City Treasurer's Office",
        "phone": "(048) 717-8012",
        "digits": "+63487178012",
        "email": "",
        "note": "Real property tax and other city payments.",
    },
    {
        "name": "City Assessor's Office",
        "phone": "(048) 717-8007",
        "digits": "+63487178007",
        "email": "",
        "note": "Property assessment records and certification.",
    },
    {
        "name": "Office of the City Civil Registrar",
        "phone": "(048) 717-8075",
        "digits": "+63487178075",
        "email": "",
        "note": "Birth, marriage, and death certificates.",
    },
    {
        "name": "City Engineering Office",
        "phone": "(048) 717-8013",
        "digits": "+63487178013",
        "email": "",
        "note": "Building permits, infrastructure, and public works.",
    },
    {
        "name": "City Agriculture Office",
        "phone": "(048) 717-8020",
        "digits": "+63487178020",
        "email": "",
        "note": "Farming, fisheries, and agricultural assistance.",
    },
    {
        "name": "City Health Office",
        "phone": "(048) 717-8084",
        "digits": "+63487178084",
        "email": "",
        "note": "Health programs, clinics, and medical assistance.",
    },
    {
        "name": "City Tourism Office",
        "phone": "(048) 717-8005",
        "digits": "+63487178005",
        "email": "",
        "note": "Visitor information, tours, and accreditation.",
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
    # Source: the official site's Contact Us page ("New City Hall Building,
    # Puerto Princesa, Philippines") and its directory page, which places the
    # key offices "at the New City Hall in Sta. Monica Heights".
    "address": (
        "New City Hall Building, Sta. Monica Heights, "
        "Puerto Princesa City, 5300 Palawan, Philippines"
    ),
    "phone": "(048) 717-8000",
    "phone_digits": "+63 48 717 8000",
    "email": "info@puertoprincesa.ph",
    "hours": "Mondays to Fridays, 8:00 AM to 5:00 PM (except regular holidays)",
    "facebook": "https://www.facebook.com/puertoprincesaph",
    # Coordinates for the New City Hall (OpenStreetMap amenity=townhall).
    # The official site's short Google Maps link resolves to a generic city
    # map, so it is not used here.
    "map_url": "https://www.google.com/maps/search/?api=1&query=9.7828847%2C118.7315522",
    "map_embed": (
        "https://maps.google.com/maps?q=9.7828847,118.7315522&z=16&output=embed"
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
            {
                "name": "Annual budget",
                "note": "The budget approved by the City Council for the current fiscal year.",
                "href": _FULL_DISCLOSURE,
            },
            {
                "name": "Statement of receipts and expenditures",
                "note": "Actual income and spending against the approved budget.",
                "href": _FULL_DISCLOSURE,
            },
            {
                "name": "Budget execution documents",
                "note": "Quarterly reports on how the budget is being used.",
                "href": _FULL_DISCLOSURE,
            },
        ],
    },
    {
        "name": "Procurement",
        "id": "procurement",
        "icon": "file-text",
        "blurb": "What the city is buying, and who it awarded the contract to.",
        "items": [
            {
                "name": "Annual procurement plan",
                "note": "Goods, works, and services the city plans to procure.",
                "href": _FULL_DISCLOSURE,
            },
            {
                "name": "Bids and awards",
                "note": "Bid notices and results from the Bids and Awards Committee.",
                "href": "https://bacoffice.puertoprincesa.ph/",
            },
            {
                "name": "Awarded contracts",
                "note": "Contracts awarded and their corresponding amounts.",
                "href": _FULL_DISCLOSURE,
            },
        ],
    },
    {
        "name": "Plans and reports",
        "id": "plans",
        "icon": "compass",
        "blurb": "The plans that guide the city's development.",
        "items": [
            {
                "name": "Comprehensive development plan",
                "note": "The city's multi-year development direction.",
                "href": _FULL_DISCLOSURE,
            },
            {
                "name": "Annual investment program",
                "note": "Programs and projects funded for the year.",
                "href": _FULL_DISCLOSURE,
            },
            {
                "name": "Executive-legislative agenda",
                "note": "Shared priorities of the mayor and the City Council.",
                "href": _FULL_DISCLOSURE,
            },
        ],
    },
    {
        "name": "Governance",
        "id": "governance",
        "icon": "award",
        "blurb": "Service standards, officials' disclosures, and performance.",
        "items": [
            {
                "name": "Citizens' Charter",
                "note": "Step-by-step service standards for every frontline office.",
                "href": "https://puertoprincesa.ph/citizens-charter/",
            },
            {
                "name": "Performance pledge",
                "note": "The service commitments the city holds itself to.",
                "href": "https://puertoprincesa.ph/performance-pledge/",
            },
            {
                "name": "SALN and financial disclosures",
                "note": "Statements of assets, liabilities, and net worth of officials.",
                "href": _FULL_DISCLOSURE,
            },
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
            "We collect what you give us directly: your name, email address, optional phone number, the topic you choose, and the message you send through this site, by email, or over the phone.",
            "Our web server also records technical information such as your IP address, browser type, the pages you visit, and the time of your visit. We use this only to keep the site secure and working.",
            "Please do not send identification numbers, health details, or other sensitive personal information through the message form. Bring those to the office instead.",
        ],
    },
    {
        "id": "use",
        "title": "How and why we use it",
        "paragraphs": [
            "We use your details to read and answer your message, route it to the office that can act on it, and keep a record of the request. We process only what is needed for that purpose.",
            "We rely on the consent you give when you tick the box before sending a message. Where the city is performing a public function, it may also rely on that lawful basis under the Data Privacy Act.",
            "We do not sell personal information, and we do not use it for advertising or profiling. We share it with another city office only when that office is the one that can help.",
        ],
    },
    {
        "id": "retention",
        "title": "How long we keep it",
        "paragraphs": [
            "Messages sent through this site are kept for two years so the city can follow up and keep a record of the request. After that they are securely deleted, unless a records law requires a longer period.",
            "Server security logs are kept for 30 days and then deleted or anonymised.",
            "If you withdraw your consent, we stop using your details for that purpose. We may keep a note that you withdrew so we do not contact you again.",
        ],
    },
    {
        "id": "third-parties",
        "title": "Who else sees your data",
        "paragraphs": [
            "The map on this site is off by default. If you choose to load it, Google receives your IP address and device information and may set its own cookies under its privacy policy. Your name, email address, and message are never sent to Google.",
            "Our hosting provider stores the site and its server logs on our behalf under a data processing agreement. If you email us, your message passes through the city's email provider.",
            "We may disclose personal information when a law requires it, or to protect someone's life or safety.",
        ],
    },
    {
        "id": "cookies",
        "title": "Cookies and tracking",
        "paragraphs": [
            "This site sets one essential cookie when you use a form. It protects the form against cross-site request forgery and does not identify you personally.",
            "There are no advertising, analytics, or social-media tracking cookies on this site.",
            'The Google map uses its own cookies only after you press "Load the map". You can block or delete cookies in your browser; the rest of the site still works.',
        ],
    },
    {
        "id": "security",
        "title": "How we protect it",
        "paragraphs": [
            "The site uses HTTPS, keeps software up to date, and limits access to personal information to staff who need it for their work.",
            "If a breach affects your personal information, the city will notify the National Privacy Commission and affected people as required by the Data Privacy Act.",
        ],
    },
    {
        "id": "rights",
        "title": "Your rights under the Data Privacy Act",
        "paragraphs": [
            "Under Republic Act No. 10173, you have the right to be informed, to object, to access, to correct, to erase or block, to damages, to file a complaint, and to data portability.",
            "To exercise any of these rights, write to the city's Data Protection Officer using the contact details below. Requests are free of charge and are acted on within the period set by the National Privacy Commission.",
            "If you are not satisfied with our response, you may file a complaint with the National Privacy Commission through privacy.gov.ph or complaints@privacy.gov.ph.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Accessibility statement
# ---------------------------------------------------------------------------

ACCESSIBILITY_FEATURES = [
    "Text and interface colours meet the WCAG 2.2 AA contrast minimum.",
    "Every page can be used with a keyboard alone, including the section navigation.",
    "Interactive parts expose their state to screen readers with ARIA attributes.",
    "Animations respect the operating system's reduced-motion setting.",
    "Images carry descriptive alternative text; decorative images are ignored.",
    "Pages are built with real headings and landmarks, so structure is announced.",
    "Tap targets are at least 24 by 24 pixels, and the main controls are 44 by 44 pixels.",
    "The site works without JavaScript, with a plain fallback for every widget.",
]

ACCESSIBILITY_SECTIONS = [
    {
        "id": "commitment",
        "title": "Our commitment",
        "paragraphs": [
            "The City Government of Puerto Princesa wants every resident to be able to use this site, including people who use screen readers, keyboard navigation, screen magnifiers, or who are deaf or hard of hearing.",
            "We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at Level AA, and we follow Republic Act No. 7277, the Magna Carta for Persons with Disability, as amended.",
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
    {
        "id": "assessment",
        "title": "How we checked this site",
        "paragraphs": [
            "Last reviewed: November 2026. We tested the redesigned site with keyboard-only navigation, a screen reader, 200% and 400% zoom, reduced-motion settings, and an automated crawl of every internal link.",
            "This statement covers the redesigned site. The previous website did not publish an accessibility statement, so there is no earlier conformance report to compare against.",
            "Found a barrier? Contact the City Information Office using the details on the Contact page. We aim to reply within five working days and to fix confirmed issues in the next release.",
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

FOI_DETAILS = {
    "officer": "Atty. Maria Lourdes D. Fernandez",
    "role": "FOI Receiving Officer",
    "email": "foi@puertoprincesa.ph",
    "phone": "(048) 717-8000 loc. 210",
    "phone_digits": "+63487178000",
    "address": (
        "New City Hall Building, Sta. Monica Heights, "
        "Puerto Princesa City, 5300 Palawan"
    ),
    "hours": "Mondays to Fridays, 8:00 AM to 5:00 PM",
}
