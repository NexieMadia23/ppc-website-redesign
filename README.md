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
       python manage.py createsuperuser
       python manage.py runserver
3. Open http://127.0.0.1:8000/admin/

## Quick checks
- Article/Event with an image but no alt text is rejected.
- Event ending before it starts is rejected.
- Service with is_external ticked and a URL not starting with https:// is rejected.

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
- `static/css/base.css` - reset, shared chrome (buttons, header, footer, emergency FAB),
  plus the `PROTOTYPE` block: emergency sheet, back-to-top, section nav, glass side rail
- `static/css/components.css` - shared design-language components (glass surfaces,
  medallions, card grids, info cards) used by every page
- `static/css/home.css` - homepage-only layout (hero, river feature, news, events, seals)
- `static/css/pages.css` - interior-page layout (page hero, breadcrumbs, timeline,
  department/office/attraction grids, safety tips)

### Interactive section navigation
Rendered from `sidebar_sections` (defined per page in `content/prototype_data.py`):
- wide screens: a fixed navy-glass rail on the right that expands on hover, keyboard
  focus, or the chevron toggle button; the active section gets a gold medallion
- narrow screens: a sticky horizontal bar
- both are driven by one scrollspy in `static/js/prototype.js` (`[data-spy] a`)

### Pages built so far
| URL | Template | Content source |
| --- | --- | --- |
| `/` | `home.html` | prototype_data |
| `/about/` | `about.html` | prototype_data |
| `/government/` | `government.html` | prototype_data |
| `/tourism/` | `tourism.html` | prototype_data |
| `/directory/` | `directory.html` | prototype_data |
| `/emergency/` | `emergency.html` | prototype_data |

### Prototype content and cleanup
- All mock/curated content lives in `content/prototype_data.py`; delete it (and the
  prototype import in `content/context_processors.py`) when the design is wired to the DB.
- Images (logo, mayor photo, seals) are hotlinked from the live city site; copy them to
  `static/img/` before launch. Only the City Hall switchboard number is verified.
- Known follow-ups: local images, favicon/Open Graph tags, EN/FIL toggle,
  News listing and article detail, Contact page.

