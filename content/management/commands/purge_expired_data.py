"""Delete personal data that has passed the published retention period.

The privacy policy tells residents that messages sent through this site are
kept for two years. This command makes that promise real: it removes old
contact messages, page feedback, and unanswered assistant questions, then
prints a short summary for the records log.

Complaints are deliberately excluded. They are case records with their own
retention schedule, so deleting them is a decision for the records officer,
not an automatic job.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import ContactMessage, FaqQuery, Feedback

DEFAULT_DAYS = 730


class Command(BaseCommand):
    help = "Delete contact messages, feedback, and assistant questions past the retention period."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=DEFAULT_DAYS,
            help=f"Retention period in days (default: {DEFAULT_DAYS} = two years).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be deleted without deleting anything.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        if days < 1:
            self.stderr.write(self.style.ERROR("--days must be a positive number."))
            return

        cutoff = timezone.now() - timedelta(days=days)
        targets = {
            "contact messages": ContactMessage.objects.filter(created_at__lt=cutoff),
            "feedback responses": Feedback.objects.filter(created_at__lt=cutoff),
            "unanswered assistant questions": FaqQuery.objects.filter(created_at__lt=cutoff),
        }

        total = 0
        for label, queryset in targets.items():
            count = queryset.count()
            total += count
            if options["dry_run"]:
                self.stdout.write(f"Would delete {count} {label} older than {days} days.")
            else:
                queryset.delete()
                self.stdout.write(f"Deleted {count} {label} older than {days} days.")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"Dry run: {total} record(s) would be removed."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Retention purge complete: {total} record(s) removed."))
