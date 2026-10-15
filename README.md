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
