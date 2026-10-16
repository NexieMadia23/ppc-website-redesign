"""Single source of truth for site pages and the main menu.

Every page listed here has a working URL, so menu and footer links can never 404.
As real pages are built in later steps, replace the placeholder view for that URL.
"""

# (url_name, url path, page title in sentence case)
PAGES = [
    ("about", "about/", "About our city"),
    ("government", "government/", "City government"),
    ("tourism", "tourism/", "Tourism"),
    ("news", "news/", "News & updates"),
    ("transparency", "transparency/", "Transparency"),
    ("directory", "directory/", "Directory"),
    ("contact", "contact/", "Contact the city"),
    ("emergency", "emergency/", "Emergency contacts"),
    ("privacy", "privacy/", "Privacy policy"),
    ("accessibility", "accessibility/", "Accessibility statement"),
    ("sitemap_page", "site-map/", "Site map"),
    ("foi", "foi/", "Freedom of information"),
]

# Top-level menu: max 7 items, in this order.
MAIN_NAV = [
    ("about", "About our city"),
    ("government", "City government"),
    ("tourism", "Tourism"),
    ("news", "News & updates"),
    ("transparency", "Transparency"),
    ("directory", "Directory"),
    ("contact", "Contact the city"),
]

# Footer links to other government sites (real, official domains).
GOV_LINKS = [
    ("GOV.PH", "https://www.gov.ph/"),
    ("Official Gazette", "https://www.officialgazette.gov.ph/"),
    ("eFOI portal", "https://www.foi.gov.ph/"),
]
