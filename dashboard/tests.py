"""Tests for the staff dashboard.

The dashboard is the private half of the hybrid admin: content editing stays in
Django admin, while charts, complaint triage, and feedback live here. These
tests pin the access rules and prove the charts are computed from the database
rather than hard-coded.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import Complaint, ComplaintUpdate, Feedback

User = get_user_model()


def make_complaint(**overrides):
    data = {
        "category": Complaint.Category.INFRASTRUCTURE,
        "subject": "Broken street light",
        "details": "The light is out.",
        "is_anonymous": True,
        "consent": True,
    }
    data.update(overrides)
    return Complaint.objects.create(**data)


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff", password="prototype-staff-2026", is_staff=True
        )
        self.resident = User.objects.create_user(
            username="resident", password="prototype-resident-2026"
        )

    def test_anonymous_visitor_is_sent_to_login(self):
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("dashboard:login"), response["Location"])
        self.assertIn("next=", response["Location"])

    def test_login_page_loads(self):
        response = self.client.get(reverse("dashboard:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff sign in")

    def test_signed_in_non_staff_gets_forbidden(self):
        self.client.force_login(self.resident)
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_open_every_dashboard_page(self):
        complaint = make_complaint()
        self.client.force_login(self.staff)
        for url in (
            reverse("dashboard:overview"),
            reverse("dashboard:complaints"),
            reverse("dashboard:complaint_detail", args=[complaint.reference]),
            reverse("dashboard:feedback"),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_dashboard_is_not_indexed(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("dashboard:overview"))
        self.assertContains(response, 'name="robots" content="noindex, nofollow"')

    def test_content_admin_links_follow_model_permissions(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("dashboard:overview"))
        self.assertNotContains(response, reverse("admin:index"))

        self.staff.user_permissions.add(Permission.objects.get(codename="view_article"))
        response = self.client.get(reverse("dashboard:overview"))
        self.assertContains(response, reverse("admin:index"))


class OverviewAggregateTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff", password="prototype-staff-2026", is_staff=True
        )
        self.client.force_login(self.staff)
        self.received = make_complaint(subject="Received one")
        self.review = make_complaint(subject="In review one")
        ComplaintUpdate.objects.create(complaint=self.review, status=Complaint.Status.IN_REVIEW)
        self.resolved = make_complaint(subject="Resolved one")
        ComplaintUpdate.objects.create(complaint=self.resolved, status=Complaint.Status.RESOLVED)
        Feedback.objects.create(page="/", helpful=True)
        Feedback.objects.create(page="/faq/", helpful=False)

    def test_kpis_come_from_the_database(self):
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.context["total_complaints"], 3)
        kpis = {item["label"]: item["value"] for item in response.context["kpis"]}
        self.assertEqual(kpis["Open complaints"], 2)
        self.assertEqual(kpis["Resolved"], 1)
        self.assertEqual(kpis["New this month"], 3)

    def test_status_donut_matches_complaint_statuses(self):
        response = self.client.get(reverse("dashboard:overview"))
        rows = {row["value"]: row["count"] for row in response.context["status_rows"]}
        self.assertEqual(rows[Complaint.Status.RECEIVED], 1)
        self.assertEqual(rows[Complaint.Status.IN_REVIEW], 1)
        self.assertEqual(rows[Complaint.Status.RESOLVED], 1)
        self.assertIn("conic-gradient", response.context["donut_gradient"])

    def test_category_and_trend_rows_are_present(self):
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.context["category_rows"][0]["value"], 3)
        self.assertEqual(len(response.context["trend"]), 6)
        self.assertEqual(response.context["feedback_total"], 2)
        self.assertEqual(response.context["feedback_unreviewed"], 2)

    def test_resolved_complaint_records_resolution_time(self):
        self.resolved.refresh_from_db()
        self.assertIsNotNone(self.resolved.resolved_at)
        self.assertLessEqual(self.resolved.resolved_at, timezone.now())


class ComplaintTriageTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff", password="prototype-staff-2026", is_staff=True
        )
        self.client.force_login(self.staff)
        self.complaint = make_complaint(subject="Pothole on Mabini Street")

    def test_list_search_matches_the_subject(self):
        response = self.client.get(reverse("dashboard:complaints"), {"q": "Mabini"})
        self.assertEqual(response.context["total"], 1)
        self.assertContains(response, "Pothole on Mabini Street")

    def test_list_filters_by_status(self):
        response = self.client.get(
            reverse("dashboard:complaints"), {"status": Complaint.Status.RESOLVED}
        )
        self.assertEqual(response.context["total"], 0)
        self.assertContains(response, "No complaints match these filters")

    def test_list_filters_by_barangay(self):
        make_complaint(subject="Other barangay", barangay="San Pedro")
        response = self.client.get(reverse("dashboard:complaints"), {"barangay": "San Pedro"})
        self.assertEqual(response.context["total"], 1)
        self.assertContains(response, "Other barangay")

    def test_status_update_is_audited_and_changes_the_complaint(self):
        response = self.client.post(
            reverse("dashboard:complaint_detail", args=[self.complaint.reference]),
            {"status": Complaint.Status.REFERRED, "note": "Sent to the district office."},
        )
        self.assertEqual(response.status_code, 302)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, Complaint.Status.REFERRED)
        update = self.complaint.updates.latest("created_at")
        self.assertEqual(update.status, Complaint.Status.REFERRED)
        self.assertEqual(update.created_by, self.staff)
        self.assertEqual(update.note, "Sent to the district office.")

    def test_invalid_status_is_rejected(self):
        response = self.client.post(
            reverse("dashboard:complaint_detail", args=[self.complaint.reference]),
            {"status": "teleported"},
        )
        self.assertEqual(response.status_code, 200)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, Complaint.Status.RECEIVED)
        self.assertEqual(self.complaint.updates.count(), 0)

    def test_staff_can_assign_a_complaint(self):
        response = self.client.post(
            reverse("dashboard:complaint_detail", args=[self.complaint.reference]),
            {"status": Complaint.Status.IN_REVIEW, "assigned_to": self.staff.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.assigned_to, self.staff)

    def test_internal_note_never_appears_on_the_public_page(self):
        self.client.post(
            reverse("dashboard:complaint_detail", args=[self.complaint.reference]),
            {
                "status": Complaint.Status.IN_REVIEW,
                "note": "Internal-only note for staff.",
            },
        )
        update = self.complaint.updates.latest("created_at")
        self.assertFalse(update.is_public)
        response = self.client.get(self.complaint.get_absolute_url())
        self.assertNotContains(response, "Internal-only note for staff.")

    def test_public_tracking_page_reflects_a_staff_update(self):
        ComplaintUpdate.objects.create(
            complaint=self.complaint,
            status=Complaint.Status.RESOLVED,
            note="Crew repaired the pothole.",
        )
        response = self.client.get(self.complaint.get_absolute_url())
        self.assertContains(response, "Crew repaired the pothole.")
        self.assertContains(response, "Resolved")


class FeedbackListTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff", password="prototype-staff-2026", is_staff=True
        )
        self.client.force_login(self.staff)
        Feedback.objects.create(page="/", helpful=True)
        Feedback.objects.create(page="/faq/", helpful=False, comment="More examples")

    def test_filters_by_response(self):
        response = self.client.get(reverse("dashboard:feedback"), {"helpful": "0"})
        self.assertEqual(response.context["total"], 1)
        self.assertContains(response, "More examples")

    def test_summary_counts_are_data_driven(self):
        response = self.client.get(reverse("dashboard:feedback"))
        self.assertEqual(response.context["total"], 2)
        self.assertEqual(response.context["positive"], 1)
        self.assertEqual(response.context["negative"], 1)
