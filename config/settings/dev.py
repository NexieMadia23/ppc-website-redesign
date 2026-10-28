from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

SITE_URL = "http://127.0.0.1:8001"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"