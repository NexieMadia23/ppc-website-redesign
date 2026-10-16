"""Bootstrap the database with the content the redesign was reviewed against.

    python manage.py migrate
    python manage.py seed_content

Idempotent: rows are matched on slug (articles, events, notices) or name
(services), so re-running it never overwrites what a staff member has since
edited through /admin/.

THIS IS THE LAST CONSUMER of the news, event, notice and service constants in
content/prototype_data.py. Delete this command together with those constants
once the real content has been entered in the database.
"""

from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from content import prototype_data
from content.models import Article, Event, Notice, Service

# The mock data labels articles with the CIO's own section name; the model stores
# the matching choice value.
CATEGORY_BY_LABEL = {label: value for value, label in Article.Category.choices}


def _aware(dt):
    """Timezone-aware when USE_TZ is on, naive otherwise."""
    return timezone.make_aware(dt) if settings.USE_TZ else dt


def _local(day, hour=8, minute=0):
    return _aware(datetime.combine(day, time(hour, minute)))


class Command(BaseCommand):
    help = "Seed the database with the prototype's curated content (safe to re-run)."

    def handle(self, *args, **options):
        self._seed_articles()
        self._seed_events()
        self._seed_notices()
        self._seed_services()
        self.stdout.write(self.style.SUCCESS("Done. Add or edit content through /admin/."))

    # -- articles --------------------------------------------------------

    def _seed_articles(self):
        created = 0
        for item in prototype_data.NEWS_ARTICLES:
            _, was_created = Article.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "summary": item["summary"],
                    "body": "\n\n".join(item["body"]),
                    "author": item["author"],
                    "category": CATEGORY_BY_LABEL.get(
                        item["category"], Article.Category.CITY_GOVERNMENT
                    ),
                    "published_at": _local(item["date"]),
                },
            )
            created += was_created
        self._report("articles", created, Article.objects.count())

    # -- events ----------------------------------------------------------

    def _seed_events(self):
        created = 0
        for item in prototype_data.EVENTS:
            clock = datetime.strptime(item["time"], "%I:%M %p").time()
            _, was_created = Event.objects.get_or_create(
                slug=slugify(item["title"])[:220],
                defaults={
                    "title": item["title"],
                    "start_datetime": _aware(datetime.combine(item["date"], clock)),
                    "venue": item["venue"],
                    "url": item["href"],
                },
            )
            created += was_created
        self._report("events  ", created, Event.objects.count())

    # -- notices ---------------------------------------------------------

    def _seed_notices(self):
        created = 0
        advisory = prototype_data.URGENT_NOTICE
        _, was_created = Notice.objects.get_or_create(
            slug=slugify(advisory["title"])[:220],
            defaults={
                "title": advisory["title"],
                "body": advisory["summary"],
                "url": advisory["href"],
                "is_urgent": True,
                "published_at": _local(date.today()),
            },
        )
        created += was_created

        for index, item in enumerate(prototype_data.NOTICES, start=1):
            _, was_created = Notice.objects.get_or_create(
                slug=slugify(item["title"])[:220],
                defaults={
                    "title": item["title"],
                    "url": item["href"],
                    # Staggered so the list keeps a sensible order.
                    "published_at": _local(date.today() - timedelta(days=3 * index)),
                },
            )
            created += was_created
        self._report("notices  ", created, Notice.objects.count())

    # -- services --------------------------------------------------------

    def _seed_services(self):
        created = 0
        groups = (
            # e-Portals serve everyone; office sites keep the model default.
            (Service.Section.PORTALS, prototype_data.EPORTALS, Service.Audience.ALL),
            (Service.Section.OFFICES, prototype_data.SERVICES, None),
        )
        for section, items, audience in groups:
            for index, item in enumerate(items, start=1):
                defaults = {
                    "description": item["description"],
                    "icon": item["icon"],
                    "url": item["href"],
                    "is_external": True,
                    "order": index * 10,
                    "section": section,
                }
                if audience is not None:
                    defaults["audience"] = audience
                _, was_created = Service.objects.get_or_create(
                    name=item["name"], defaults=defaults
                )
                created += was_created
        self._report("services ", created, Service.objects.count())

    # -- output ----------------------------------------------------------

    def _report(self, label, created, total):
        self.stdout.write(f"{label}: {created} created, {total} in total")
