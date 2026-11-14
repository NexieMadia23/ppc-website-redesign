import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # fails loudly if missing
DEBUG = False

# Railway publishes the service domain automatically. Add it to the allowed
# hosts so the app works after the first deploy without a second settings edit.
RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
RAILWAY_PRIVATE_DOMAIN = os.environ.get("RAILWAY_PRIVATE_DOMAIN", "").strip()
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]
if RAILWAY_PUBLIC_DOMAIN and RAILWAY_PUBLIC_DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
    # Covers the edge hostname Railway uses for its own health checks.
    ALLOWED_HOSTS.append(".up.railway.app")
if RAILWAY_PRIVATE_DOMAIN and RAILWAY_PRIVATE_DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RAILWAY_PRIVATE_DOMAIN)
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "content",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "content.context_processors.site",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Railway's Postgres plugin exposes DATABASE_URL. Without it (local SQLite,
# tests) the block above is kept.
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.parse(
        os.environ["DATABASE_URL"],
        conn_max_age=600,
        conn_health_checks=True,
    )

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization (English + Filipino)
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("fil", "Filipino")]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# Static and media. WhiteNoise serves STATIC_ROOT after collectstatic.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"

# Railway volumes are ephemeral unless a volume is attached. When one is
# mounted, keep uploads under <mount>/media so they survive a redeploy.
_volume_mount = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "").strip()
_default_media_root = Path(_volume_mount) / "media" if _volume_mount else BASE_DIR / "media"
MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", _default_media_root))

# Site identity. Phone/email are optional: leave blank and they are simply hidden,
# so the header can never show a broken tel: or mailto: link.
SITE_NAME = "City Government of Puerto Princesa"
# Absolute origin used in robots.txt and canonical links. On Railway this
# follows the generated domain; set DJANGO_SITE_URL for a custom domain.
_default_site_url = (
    f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else "http://localhost:8020"
)
SITE_URL = os.environ.get("DJANGO_SITE_URL", _default_site_url).rstrip("/")
SITE_PHONE = os.environ.get("SITE_PHONE", "").strip()
SITE_EMAIL = os.environ.get("SITE_EMAIL", "").strip()

# Cache-backed throttling for public forms. Turn it off only for load tests or
# in a test suite that deliberately submits many forms from one address.
RATE_LIMITS_ENABLED = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Staff dashboard authentication. Residents never need an account; they submit
# and track complaints with a reference number.
LOGIN_URL = "dashboard:login"
LOGIN_REDIRECT_URL = "dashboard:overview"
LOGOUT_REDIRECT_URL = "home"
