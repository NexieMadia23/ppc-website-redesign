# Puerto Princesa City Government website: Step 1

Django 5.2 LTS project foundation (settings split, models, admin).

## Setup (Windows PowerShell)
    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    copy .env.example .env

## Setup (macOS/Linux)
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

## Then
1. Generate a secret key and paste it into `.env` as DJANGO_SECRET_KEY:
       python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
2. Run:
       python manage.py makemigrations content
       python manage.py migrate
       python manage.py seed_content
       python manage.py createsuperuser
       python manage.py runserver
3. Open http://127.0.0.1:8000/admin/

`seed_content` is optional and safe to re-run: it fills the news, events, notices
and services tables once, and never overwrites rows you have since edited.

## Quick checks
- Article/Event with an image but no alt text is rejected.
- Event ending before it starts is rejected.
- Service with is_external ticked and a URL not starting with https:// is rejected.
- Any link field rejects `tempmain.puertoprincesa.ph` / `staging` URLs, and must be
  either an internal `/path/` or a full `https://` address.

PythonAnywhere free tier: web app expires every 1 month (extend it), 512 MiB disk,
SQLite only on newer accounts.

## Step 2: base template and design system
- Design tokens: static/css/tokens.css (the only place colours, spacing, type are set)
- Components and layout: static/css/base.css; menu toggle: static/js/main.js
- Templates: templates/base.html and templates/partials/ (header, footer, icons)
- Menu and page list: content/navigation.py (every link has a working URL)
- Optional header phone/email: set SITE_PHONE and SITE_EMAIL in .env (hidden when blank)
- Pages like /residents/ are temporary placeholders until their step is built.

## Prototype branch (`prototype`)
Redesign in progress. `main` keeps the clean foundation; all design work lives here and
is marked with `PROTOTYPE` comments so it can be reviewed, then merged or dropped.

### Design language ("glamorphism")
Navy `#09246D` / gold `#F1BC02` / periwinkle `#7081BF` / cloud `#D5D4D2`, with frosted
glass surfaces. Gold surfaces always use navy text (white-on-gold fails contrast).

### Stylesheets
- `static/css/tokens.css` - palette, type, spacing, glass tokens (single source of truth)
- `static/css/base.css` - reset, shared chrome (buttons, header, footer), plus the
  `PROTOTYPE` block: emergency sheet, reveal-on-scroll, floating page nav, and the
  floating action stack (back-to-top + emergency)
- `static/css/components.css` - shared design-language components (glass surfaces,
  medallions, card grids, info cards) used by every page
- `static/css/home.css` - homepage-only layout (hero, river feature, news, events, seals)
- `static/css/pages.css` - interior-page layout (page hero, breadcrumbs, timeline,
  department/office/attraction grids, safety tips)

### Interactive section navigation
One floating nav, rendered from `sidebar_sections` (set per page in
`content/views.py`) plus one City Hotlines action, with three responsive shapes.
Frosted glass throughout rather than a solid navy slab, so the chrome stays
light whatever the page behind it is doing:
- phones (<= 767px): a single round glass Menu button on the bottom edge, inside
  thumb reach. Tapping it dims the page (`--scrim`), holds the page still against
  scrolling and lifts the button to the middle of the screen, where every item of
  the page rings it at a fixed radius as its own 44px frosted-glass medallion
  with the label underneath. A full ring - not a row or a half fan - is what lets
  all eight labelled items fit around one hub on a 320px phone: no sideways
  scroll, no hidden item, no truncated label, and no two items on the same spot.
  The ring is placed entirely in CSS (`--nav-n` on the list, `--i` per item), so a
  short page keeps a tidy ring and a longer one simply spreads out. Without
  JavaScript the ring is always open, so every item stays reachable.
- tablets (768-1023px): a compact light-glass rail pinned to the right edge
- desktops (>= 1024px): the same rail with more breathing room, which expands on
  hover, keyboard focus, or the chevron toggle button and shows a tooltip
  (`title`) per link; the active section gets a gold medallion
- all three are driven by one scrollspy in `static/js/prototype.js` (`[data-spy] a`)

The header keeps only the brand, the nav and the search bar - the City Hotlines
button moved into this menu, so it is one link rather than a second entrance.

### Floating action stack
`back-to-top`, the emergency button and the Menu button read as one deliberate
vertical column. On phones the column is centred on the Menu button and stacks
Back-to-top, Emergency, Menu with the same 20px gap (`--fab-gap`) between every
pair, so nothing overlaps, drifts into a corner or blocks page content; wider
screens keep the column in the bottom-right safe area. All three are fully
rounded and share one blur, border and shadow scale, and they are sized to show
hierarchy at a glance: the Menu button is the largest (`--fab`, 56px), the
emergency button matches it, and back-to-top is deliberately the smallest
(`--fab-sm`, 44px). Emergency stays out of navigation - it is a quick dial to the
emergency page, and the separate City Hotlines entry in the menu is a plain link
to the directory. The right-hand rail caps its height at `100vh - 18rem` so a
long section list can never reach the stack. Fixed-chrome layering is one
documented scale in `tokens.css`: `--z-nav` (850) < `--z-actions` (900) <
`--z-scrim` (940) < `--z-nav-open` (950) < `--z-skip` (1000); dialogs use the
top layer.

### Template gotcha: multi-line `{# ... #}` comments
Django only strips **single-line** `{# ... #}` comments. A comment that wraps
across lines is rendered verbatim as visible text on the page. Write each line
as its own `{# ... #}` comment (or use `{% comment %} ... {% endcomment %}`), and
rely on `SiteIntegrityTests.test_no_page_leaks_template_syntax_or_unicode_tricks`,
which fails on a leaked `{#` or `#}`.

### Pages built so far
Every page in the menu, footer, and site map is now a real prototype page (no
placeholders remain).

| URL | Template | Content source |
| --- | --- | --- |
| `/` | `home.html` | DB (news, notices, events, services) + prototype_data (city facts, festivals, seals) |
| `/about/` | `about.html` | prototype_data |
| `/government/` | `government.html` | prototype_data |
| `/tourism/` | `tourism.html` | prototype_data |
| `/news/` | `news.html` | DB, paginated and filterable by `?category=` |
| `/news/<slug>/` | `news_detail.html` | DB (404 for unknown or future-dated slugs) |
| `/transparency/` | `transparency.html` | prototype_data (`TRANSPARENCY_GROUPS`) |
| `/directory/` | `directory.html` | DB (`DirectoryOffice`, `EmergencyContact`) |
| `/contact/` | `contact.html` | DB (`ContactDetails`, `ContactTopic`, `ContactFaq`) |
| `/emergency/` | `emergency.html` | DB (`EmergencyContact`, `SafetyTip`) |
| `/foi/` | `foi.html` | prototype_data (`FOI_*`) |
| `/privacy/` | `privacy.html` | prototype_data (`PRIVACY_SECTIONS`) |
| `/accessibility/` | `accessibility.html` | prototype_data (`ACCESSIBILITY_*`) |
| `/site-map/` | `sitemap.html` | generated from `content/navigation.py` |

Notes:
- The site map is generated from `PAGES`/`MAIN_NAV`, so it can never drift from the menu.
- The contact form is a mockup: `prototype.js` intercepts submit and shows a confirmation;
  with JavaScript off the POST re-renders the page, so nothing errors either way.
- `content/views.py` still keeps `views.placeholder` so a page added to `PAGES` without a
  view resolves instead of 404-ing.

## Phase 1: the news data layer (branch `nexie`)

News, events, notices and services now come from the database instead of
`prototype_data`. The templates are visually unchanged: the models expose the
same names the templates already used (`article.date`, `event.time`,
`article.paragraphs`) as properties.

- **Models** (`content/models.py`)
  - `Article.author`; `body` is plain text split on blank lines by
    `Article.paragraphs`.
  - `Article.category` is the CIO's own section: City government, City Council,
    Tourism, Health, Advisory, Press release, Announcement.
  - `Event.description` optional, `Event.url` added; `Notice.url` added. Both
    `url` fields are optional, and the templates render a plain title when
    they are blank so an empty `href` can never appear.
  - `Service.section` separates the homepage's e-Portal row from the city
    offices and attractions.
  - `validate_link()` rejects staging/temporary domains and requires either an
    internal `/path/` or a full `https://` address.
  - `Article.objects.published()` hides future-dated stories (404 on their own
    URL too); `Event.objects.upcoming()` drops events that already started.
- **Views** (`content/views.py`): `home`, `news`, `news_detail` query the DB.
  `/news/?page=` paginates (`NEWS_PER_PAGE`, 6) and `/news/?category=`
  filters by section. Both are query parameters, so the menu and the generated
  site map are unaffected.
- **Seed**: `python manage.py seed_content` — 6 articles, 3 events, 4 notices
  (one urgent advisory), 8 services. Idempotent, matched on slug/name.
- **Tests**: `python manage.py test content` — visibility, pagination,
  filtering, homepage ordering, link integrity, URL validation.

Follow-ups for Phase 1: nothing pending. Content itself needs review through
`/admin/` — the seeded rows are the headlines the design was reviewed against,
and `prototype_data` only supplies what the later slices deliberately left out
(transparency, festivals, city profile).

## Phase 2 and beyond

Directory, contact, transparency, festivals and city profile are moving from
`content/prototype_data.py` onto models, one cluster at a time (see the table
above for which template reads what).

### Slice A done: the contacts cluster
`DirectoryOffice`, `EmergencyContact`, `SafetyTip`, `ContactDetails` (a
singleton), `ContactTopic` and `ContactFaq` now back `/directory/`,
`/emergency/` and `/contact/`. `EmergencyContact` also feeds the quick-dial
sheet that every page carries, so `content/context_processors.py` no longer
imports `prototype_data`. Migration `0003`. The seed command fills these rows
from the same constants; `ContactDetails.load()` returns a sane default when the
single row has not been created yet, so a page never 500s. Tests pin the
ordering, the `tel:` digit rules, the singleton, and that these pages no longer
show prototype copy.

### Remaining slices
- Slice B: city profile, facts, history, government pillars and departments,
  mayor, attractions, travel tips, festivals (the `/about/`, `/government/`,
  `/tourism/` and remaining homepage blocks).
- Slice C: transparency, then a versioned content module for the legal pages
  (privacy, accessibility, FOI) and the per-page sidebars, then delete
  `content/prototype_data.py`, `static/js/prototype.js` and the `PROTOTYPE`
  comments/notes.

### Prototype content and cleanup
- Images (logo, mayor photo, seals) are hotlinked from the live city site; copy them to
  `static/img/` before launch. Only the City Hall switchboard number is verified.
- Legal text on `/privacy/`, `/accessibility/`, and `/foi/` is draft wording for design
  review and needs sign-off before launch.
- Known follow-ups: local images, favicon/Open Graph tags, EN/FIL toggle, a physical
  address confirmation, and wiring each page to real DB queries.

