"""Single source of truth for site pages and the main menu.

Every page listed here has a working URL, so menu and footer links can never 404.
As real pages are built in later steps, replace the placeholder view for that URL.
"""

# (url_name, url path, page title in sentence case)
PAGES = [
    ("residents", "residents/", "Residents"),
    ("business", "business/", "Business"),
    ("visitors", "visitors/", "Visitors"),
    ("government", "government/", "Government"),
    ("transparency", "transparency/", "Transparency"),
    ("news", "news/", "News & updates"),
    ("contact", "contact/", "Contact"),
    ("emergency", "emergency/", "Emergency contacts"),
    ("privacy", "privacy/", "Privacy policy"),
    ("accessibility", "accessibility/", "Accessibility statement"),
    ("sitemap_page", "site-map/", "Site map"),
    ("foi", "foi/", "Freedom of information"),
]

# Top-level menu: max 7 items, in this order.
MAIN_NAV = [
    ("residents", "Residents"),
    ("business", "Business"),
    ("visitors", "Visitors"),
    ("government", "Government"),
    ("transparency", "Transparency"),
    ("news", "News & updates"),
    ("contact", "Contact"),
]

# Footer links to other government sites (real, official domains).
GOV_LINKS = [
    ("GOV.PH", "https://www.gov.ph/"),
    ("Official Gazette", "https://www.officialgazette.gov.ph/"),
    ("eFOI portal", "https://www.foi.gov.ph/"),
]
