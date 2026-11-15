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

## Deploy on Railway

`railway.json` configures the build and deploy (RAILPACK, Gunicorn, health
check at `/healthz/`). The app reads these environment variables:

| Variable | Required | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | yes | Django secret; the app refuses to start without it |
| `DJANGO_SETTINGS_MODULE` | recommended | Set to `config.settings.prod` so shell commands use production settings |
| `DATABASE_URL` | yes (Railway Postgres) | Injected when you add the PostgreSQL plugin |
| `DJANGO_ALLOWED_HOSTS` | no | Extra comma-separated hosts for a custom domain |
| `DJANGO_SITE_URL` | no | Canonical origin, e.g. `https://puertoprincesa.example` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | no | Extra `https://...` origins for a custom domain |

Steps:

1. Push the repo to GitHub and create a Railway project from it.
2. Add the **PostgreSQL** plugin; Railway sets `DATABASE_URL` automatically.
   The generated `*.up.railway.app` domain is detected from
   `RAILWAY_PUBLIC_DOMAIN`, so no host edit is needed.
3. Set `DJANGO_SECRET_KEY` and `DJANGO_SETTINGS_MODULE=config.settings.prod`
   in the service variables.
4. Deploy. The pre-deploy command runs `migrate` and `collectstatic`.
5. In the service shell, run `python manage.py seed_demo` (or
   `seed_demo --with-users` for the demo accounts) and
   `python manage.py createsuperuser` if the database is empty.
6. **Media uploads**: without a volume they are lost on redeploy. Attach a
   Railway volume mounted at `/data`; `MEDIA_ROOT` then becomes `/data/media`
   and the app serves `/media/` itself (WhiteNoise only handles static files).

## Step 2: base template and design system
- Design tokens: static/css/tokens.css (the only place colours, spacing, type are set)
- Shared chrome: static/css/base.css (masthead, visible desktop nav, full-screen menu on phones, footer)
- Components and layout: static/css/components.css and the per-page stylesheets
- Templates: templates/base.html and templates/partials/ (header, footer, icons)
- Menu and page list: content/navigation.py (every link has a working URL)
- Optional header phone/email: set SITE_PHONE and SITE_EMAIL in .env (hidden when blank)
- Pages like /residents/ are temporary placeholders until their step is built.

## Design language: blue, yellow, white
The whole site is one system; the palette has a single source of truth in
`static/css/tokens.css`:

- **Blue** carries structure: `--blue-50` … `--blue-950`, with `--color-dominant`
  (`#0B3F91`) for headers, navigation, footers, and primary actions.
- **Yellow** carries emphasis: `--yellow-50` … `--yellow-900`, with
  `--color-accent` (`#F7C600`) for section rules, active states, and highlights.
- **White / cool neutrals** carry content: `--neutral-0` … `--neutral-950` and the
  semantic roles `--color-bg`, `--color-surface`, `--color-surface-raised`.

Components consume semantic roles (`--color-dominant`, `--color-secondary`,
`--color-accent`, `--color-text`, `--color-border`) rather than raw hex values.
The legacy `--color-primary*` names remain as aliases for older rules, but new
work should use the semantic names.

Glass is a tokenised surface, not a per-page effect: `--glass-bg`,
`--glass-bg-strong`, `--glass-border`, `--glass-highlight`, `--glass-shadow`,
and `--glass-blur` (`blur(20px) saturate(165%)`). It is reserved for surfaces
that sit over photography or other artwork; cards, forms, tables, and search
results use flat bordered surfaces. Dark blue sections use the
`--glass-dark-*` set instead.

Contrast is checked against WCAG 2.1 AA: body text 14.7:1, muted text 5.5:1,
white on dominant blue 9.8:1, dominant blue on yellow 8.0:1. Yellow surfaces
always use dark blue text; white on yellow is never used.

### Stylesheets
- `static/css/tokens.css` - palette, type, spacing, glass tokens (single source of truth)
- `static/css/base.css` - reset, shared chrome (buttons, masthead, nav, mobile menu,
  footer), the emergency sheet, and back-to-top
- `static/css/components.css` - shared components used by every page (buttons, cards,
  ledgers, feature and step rows, index bars, chat widget, forms)
- `static/css/home.css` - homepage-only art direction (hero, service bar, news, events,
  photo gallery, seals)
- `static/css/pages.css` - interior-page styles (page hero, breadcrumbs, timeline,
  department/attraction rows, legal text) plus the complaint, directory, search,
  and FAQ blocks
- `static/css/dashboard.css` - staff dashboard only (shell, KPIs, CSS/SVG charts, tables)
- `static/js/app.js` - FAQ assistant, voice search, anonymous toggle, FAQ filter,
  and AJAX page feedback (all client-side, no external services)
- `static/js/site.js` - emergency quick-dial sheet, mobile menu, FAQ chat panel,
  scroll effects, count-up statistics, complaint steps, and map consent

### Pages built so far
Every page in the menu, footer, and site map is now a real prototype page (no
placeholders remain).

| URL | Template | Content source |
| --- | --- | --- |
| `/` | `home.html` | database first, prototype_data fallback |
| `/about/` | `about.html` | prototype_data |
| `/government/` | `government.html` | Office rows + prototype_data pillars |
| `/tourism/` | `tourism.html` | prototype_data |
| `/news/` | `news.html` | database first, prototype_data fallback |
| `/news/<slug>/` | `news_detail.html` | database first, prototype_data fallback |
| `/transparency/` | `transparency.html` | prototype_data (`TRANSPARENCY_GROUPS`) |
| `/directory/` | `directory.html` | Agency/Office rows, prototype_data fallback |
| `/contact/` | `contact.html` | prototype_data (`CONTACT_*`) |
| `/emergency/` | `emergency.html` | prototype_data |
| `/foi/` | `foi.html` | prototype_data (`FOI_*`) |
| `/privacy/` | `privacy.html` | prototype_data (`PRIVACY_SECTIONS`) |
| `/accessibility/` | `accessibility.html` | prototype_data (`ACCESSIBILITY_*`) |
| `/site-map/` | `sitemap.html` | generated from `content/navigation.py` |
| `/sumbungan/` | `sumbungan.html` | `ComplaintForm` -> `Complaint` |
| `/sumbungan/track/` | `complaint_track.html` | `Complaint.reference` lookup |
| `/sumbungan/track/<reference>/` | `complaint_track_detail.html` | `Complaint` + updates |
| `/faq/` | `faq.html` | `content/faq.py` |
| `/search/` | `search.html` | DB records with prototype fallback |
| `/photo-credits/` | `photo_credits.html` | `PHOTO_CREDITS` |
| `/dashboard/` | `dashboard/*.html` | staff only (`login_required` + `is_staff`) |

Notes:
- The site map is generated from `PAGES`/`MAIN_NAV`, so it can never drift from the menu.
- The contact form saves each message as a `ContactMessage` (admin-visible) and redirects
  back with a success message; no email is sent in the prototype.
- `content/views.py` still keeps `views.placeholder` so a page added to `PAGES` without a
  view resolves instead of 404-ing.

### Complaints, directory, search, and staff dashboard
- **Sumbungan ng Bayan** (`/sumbungan/`): residents submit a complaint without an account,
  optionally anonymously. The form routes it to an agency, generates a `PPC-YYYY-######`
  reference, and writes the first `ComplaintUpdate`. Residents track it at
  `/sumbungan/track/`; contact details are never shown on the public tracking page.
- **Directory** (`/directory/`): reads `Agency`/`Office` rows from the database, with search
  and agency filters. Prototype data is the fallback when the database is empty.
- **Search** (`/search/`): text or voice (Web Speech API) query across services, offices,
  news, events, notices, documents, FAQs, and pages, with kind filters and a no-results path.
- **FAQ assistant**: `content/faq.py` is a keyword/FAQ matcher. The chat widget and `/faq/ask/`
  reuse it; it never calls an AI service and says so when it has no answer.
- **Hybrid admin**: content editing stays in Django admin; `/dashboard/` is the staff-only
  view for KPI cards, CSS/SVG charts from ORM aggregates, complaint triage, and feedback.
  Anonymous visitors are redirected to `/dashboard/login/`; signed-in non-staff get a 403.
  Content-admin links only appear when the account has the matching model permission.
- **Demo data**: `python manage.py seed_demo --with-users` creates the seed records plus
  `staff` / `prototype-staff-2026` and `admin` / `prototype-admin-2026`. The demo staff
  account has view/add/change rights on content models; delete stays with the superuser.
- **Prototype limits**: no email/SMS is sent, no agency API is called, and no live AI or
  real-time sync is used. Feedback and complaint status changes are local database writes.

### Photography and credits
Local, optimized photos live in `static/img/photos/` (WebP with a JPEG fallback).
The homepage hero is a three-photo cross-fade of official city video stills, and
the tourism cards, the About page, and the homepage "The city in photos" strip
use the same library. The hero photos are eager/lazy loaded and the cross-fade
stops for reduced-motion visitors.

The About page is the most visual interior page: a three-photo profile collage,
a 66-dot barangay grid showing the 35 urban / 31 rural split and the land each
takes up, a travel/access strip, a six-photo mosaic, and culture cards. All
images are local and lazy loaded except the first collage photo.

News cards and article pages use official City Government photos stored in
`static/img/news/`. Per-photo credit text is kept off the content pages: the footer
has a short "Photographs" line linking to `/photo-credits/`, which lists every
author, licence, and source. Sources are the City Government of Puerto Princesa
and Wikimedia Commons:

| Photo | Author | Licence |
| --- | --- | --- |
| Balayong hero stills | City Government of Puerto Princesa | Official city video still |
| Subaraw 2026 news photos | City Government of Puerto Princesa | Official city photo |
| City Baywalk | Patrickroque01 | CC BY-SA 4.0 |
| Underground River | lumoplank | CC0 |
| Sabang Beach | Patrickroque01 | CC BY-SA 4.0 |
| Immaculate Conception Cathedral | Herbertkikoy | CC BY-SA 4.0 |
| Iwahig River | Filipinayzd | CC BY-SA 4.0 |
| Subterranean River limestone | Vyacheslav Argenberg | CC BY 4.0 |
| Honda Bay (Luli Island) | mendhak | CC BY-SA 2.0 |
| Plaza Cuartel | Patrickroque01 | CC BY-SA 4.0 |
| Baker's Hill | shankar s. | CC BY 2.0 |
| Puerto Princesa Airport | Luisztdt | CC BY-SA 4.0 |

### Prototype content and cleanup
- All mock/curated content lives in `content/prototype_data.py`; delete it (and the
  prototype import in `content/context_processors.py`) when the design is wired to the DB.
- The mayor portrait, honours/seals row, hero photos, and news photos are local
  copies under `static/`. Only the City Hall switchboard number is verified.
- Legal text on `/privacy/`, `/accessibility/`, and `/foi/` is draft wording for design
  review and needs sign-off before launch.
- Known follow-ups: favicon/Open Graph tags, EN/FIL toggle, a physical address
  confirmation, and wiring each page to real DB queries.

