"""Small, dependency-free rate limiting for public forms and endpoints.

The site runs on a single small host, so a cache-backed counter per client IP is
enough to stop accidental double submissions and simple form spam. It is not a
defence against a distributed attack; that belongs at the proxy or firewall.

Callers treat a limited request as a normal validation failure so residents see
a clear message instead of a stack trace.
"""

from django.conf import settings
from django.core.cache import cache

# How long a block lasts, in seconds. Windows are deliberately generous: a real
# resident rarely sends more than a handful of messages an hour.
WINDOWS = {
    "contact": (5, 60 * 60),
    "feedback": (20, 60 * 60),
    "sumbungan": (5, 60 * 60),
    "track": (20, 60 * 60),
    "faq": (40, 60),
}


def client_ip(request):
    """Best-effort client address, honouring a single trusted proxy header."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or "unknown"


def is_limited(request, bucket):
    """Count this request against ``bucket`` and return ``True`` once over."""
    if not getattr(settings, "RATE_LIMITS_ENABLED", True):
        return False
    limit, window = WINDOWS[bucket]
    key = f"ratelimit:{bucket}:{client_ip(request)}"
    added = cache.add(key, 1, window)
    if added:
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        # The key expired between add() and incr(); start a fresh window.
        cache.set(key, 1, window)
        return False
    return count > limit


def reset():
    """Test helper: clear every counter (the cache is per-process anyway)."""
    cache.clear()
