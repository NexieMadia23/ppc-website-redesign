"""Single source of truth for site pages and the main menu.

Every page listed here has a working URL, so menu and footer links can never 404.
As real pages are built in later steps, replace the placeholder view for that URL.
"""

# (url_name, url path, page title in sentence case)
PAGES = [
    ("about", "about/", "About our city"),
    ("government", "government/", "Government"),
    ("tourism", "tourism/", "Tourism"),
    ("news", "news/", "News & updates"),
    ("transparency", "transparency/", "Transparency"),
    ("directory", "directory/", "Directory"),
    ("contact", "contact/", "Contact"),
    ("emergency", "emergency/", "Emergency contacts"),
    ("privacy", "privacy/", "Privacy policy"),
    ("accessibility", "accessibility/", "Accessibility statement"),
    ("sitemap_page", "site-map/", "Site map"),
    ("foi", "foi/", "Freedom of information"),
    ("faq", "faq/", "Frequently asked questions"),
]

# Top-level menu, modelled on the live city site's header. Each item is a
# dict so a section can carry a dropdown:
#   name:     URL name for internal pages (None for an external-only item)
#   label:    text shown in the bar
#   url:      external URL, used when name is None
#   children: optional submenu entries, resolved by the context processor.
#             A child uses either name + optional anchor, or a raw url.
MAIN_MENU = [
    {"name": "home", "label": "Home"},
    {
        "name": "about",
        "label": "About our city",
        "children": [
            {"label": "City profile", "name": "about", "anchor": "profile"},
            {"label": "Key facts", "name": "about", "anchor": "facts"},
            {"label": "Photo gallery", "name": "about", "anchor": "gallery"},
            {"label": "History", "name": "about", "anchor": "history"},
            {
                "label": "People and culture",
                "name": "about",
                "anchor": "culture",
            },
        ],
    },
    {
        "name": "government",
        "label": "Government",
        "children": [
            {
                "label": "How it is organised",
                "name": "government",
                "anchor": "pillars",
            },
            {
                "label": "The city mayor",
                "name": "government",
                "anchor": "council",
            },
            {
                "label": "City departments",
                "name": "government",
                "anchor": "departments",
            },
            {"label": "Directory of offices", "name": "directory"},
        ],
    },
    {
        "name": "tourism",
        "label": "Tourism",
        "children": [
            {
                "label": "Top attractions",
                "name": "tourism",
                "anchor": "attractions",
            },
            {
                "label": "Underground River",
                "name": "tourism",
                "anchor": "river",
            },
            {
                "label": "Festival calendar",
                "name": "tourism",
                "anchor": "festivals",
            },
            {"label": "Travel tips", "name": "tourism", "anchor": "tips"},
        ],
    },
    {"name": "news", "label": "News & updates"},
    {"name": "transparency", "label": "Transparency"},
    {
        "name": "directory",
        "label": "Directory",
        "children": [
            {
                "label": "Emergency hotlines",
                "name": "directory",
                "anchor": "hotlines",
            },
            {"label": "City offices", "name": "directory", "anchor": "offices"},
            {"label": "Emergency contacts", "name": "emergency"},
        ],
    },
    {"name": "contact", "label": "Contact"},
    {
        # Real e-government services listed on the live city site.
        "label": "e-Services",
        "url": "https://www.filipizen.com/partners/palawan_puertoprincesa",
        "children": [
            {
                "label": "E-Payment",
                "url": "https://www.filipizen.com/partners/palawan_puertoprincesa",
            },
            {
                "label": "CGPP Service Desk",
                "url": "https://cgpp.online/servicerequest",
            },
            {
                "label": "Legislative Tracking System",
                "url": "https://puertoprincesa.ph/legislative-tracking-system/",
            },
            {"label": "City Building", "url": "https://ocbo.puertoprincesa.ph/"},
            {
                "label": "City Tourism",
                "url": "https://citytourism.puertoprincesa.ph/",
            },
            {
                "label": "Bids and Awards",
                "url": "https://bacoffice.puertoprincesa.ph/",
            },
        ],
    },
]

# Flat list of internal sections, kept for the site map and older callers.
MAIN_NAV = [
    (item["name"], item["label"]) for item in MAIN_MENU if item.get("name")
]

# Slim utility strip above the masthead, like the links at the top of the
# live city site.
UTILITY_LINKS = [
    ("GOV.PH", "https://www.gov.ph/"),
    ("E-Payment", "https://www.filipizen.com/partners/palawan_puertoprincesa"),
    ("eFOI", "https://www.foi.gov.ph/"),
]

# Footer links to other government sites (real, official domains).
GOV_LINKS = [
    ("GOV.PH", "https://www.gov.ph/"),
    ("Official Gazette", "https://www.officialgazette.gov.ph/"),
    ("eFOI portal", "https://www.foi.gov.ph/"),
]
