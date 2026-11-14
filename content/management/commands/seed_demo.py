"""Seed the prototype with realistic demo data.

Usage:
    python manage.py seed_demo
    python manage.py seed_demo --with-users

The command is idempotent: running it twice updates the same records instead of
creating duplicates. ``--with-users`` also creates a demo staff account and a
demo superuser, which are handy for reviewing the staff dashboard.
"""

from datetime import date, datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from content import prototype_data
from content.models import (
    Agency,
    Article,
    Complaint,
    ComplaintUpdate,
    ContactMessage,
    Document,
    Event,
    Feedback,
    Notice,
    Office,
    Service,
)

AGENCIES = [
    ("City Engineer's Office", Agency.Category.INFRASTRUCTURE, "Roads, drainage, and public works"),
    (
        "City Environment and Natural Resources Office",
        Agency.Category.ENVIRONMENT,
        "Trees, waterways, and pollution",
    ),
    ("City Health Office", Agency.Category.HEALTH, "Clinics, sanitation, and health programs"),
    (
        "City Social Welfare and Development Office",
        Agency.Category.SOCIAL,
        "Assistance for families, seniors, and PWDs",
    ),
    ("City Treasurer's Office", Agency.Category.BUSINESS, "Taxes, payments, and business permits"),
    (
        "City Disaster Risk Reduction and Management Office",
        Agency.Category.SAFETY,
        "Disaster response and rescue",
    ),
    ("City Tourism Office", Agency.Category.OTHER, "Visitor information and tourism concerns"),
]


def aware(day, hour=9):
    return timezone.make_aware(datetime.combine(day, time(hour=hour)))


class Command(BaseCommand):
    help = "Create demo agencies, offices, documents, complaints, and feedback."

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-users",
            action="store_true",
            help="Also create demo staff and superuser accounts.",
        )

    def handle(self, *args, **options):
        agencies = self.seed_agencies()
        self.seed_services()
        self.seed_offices(agencies)
        self.seed_documents()
        self.seed_content()
        self.seed_complaints(agencies)
        self.seed_feedback()
        self.seed_contact_messages()
        if options["with_users"]:
            self.seed_users()
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))

    def seed_agencies(self):
        agencies = {}
        for order, (name, category, description) in enumerate(AGENCIES, start=1):
            agency, _ = Agency.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "name": name,
                    "category": category,
                    "description": description,
                    "email": "info@puertoprincesa.ph",
                    "order": order,
                },
            )
            agencies[category] = agency
        return agencies

    def seed_services(self):
        services = []
        for item in prototype_data.EPORTALS + prototype_data.SERVICES:
            service, _ = Service.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "icon": item.get("icon", ""),
                    "url": item["href"],
                    "is_external": item["href"].startswith("http"),
                    "audience": Service.Audience.ALL,
                },
            )
            services.append(service)
        return services

    def seed_offices(self, agencies):
        for order, item in enumerate(prototype_data.DIRECTORY_OFFICES, start=1):
            Office.objects.update_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "name": item["name"],
                    "description": item["note"],
                    "phone": item["phone"],
                    "phone_digits": item["digits"],
                    "email": item["email"],
                    "is_emergency": False,
                    "order": order,
                },
            )
        for order, item in enumerate(prototype_data.EMERGENCY_CONTACTS, start=1):
            Office.objects.update_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "name": item["name"],
                    "description": item["note"],
                    "phone": item["number"],
                    "phone_digits": item["digits"],
                    "is_emergency": True,
                    "order": order,
                },
            )

    def seed_documents(self):
        samples = [
            ("Annual Budget Report 2026", Document.Category.BUDGET, 2026),
            ("Bids and Awards Summary, Q3 2026", Document.Category.BIDS, 2026),
            ("City Ordinance Index 2025", Document.Category.ORDINANCE, 2025),
            ("Full Disclosure Report 2025", Document.Category.REPORT, 2025),
            ("FOI Request Log 2025", Document.Category.FOI, 2025),
            ("Citizens' Charter 2025", Document.Category.OTHER, 2025),
            ("Annual Investment Program 2026", Document.Category.BUDGET, 2026),
            ("Statement of Receipts and Expenditures, Q2 2026", Document.Category.BUDGET, 2026),
            ("Invitation to Bid: City Health Center Annex", Document.Category.BIDS, 2026),
            ("Award Notice: Barangay Road Concreting", Document.Category.BIDS, 2026),
            ("Resolution No. 2026-118, Coastal Protection", Document.Category.ORDINANCE, 2026),
            ("Ordinance No. 2026-07, Plastic Regulation", Document.Category.ORDINANCE, 2026),
            ("Annual Governance Report 2025", Document.Category.REPORT, 2025),
            ("Local Disaster Risk Reduction Plan 2026", Document.Category.REPORT, 2026),
            ("FOI Request Log, First Half 2026", Document.Category.FOI, 2026),
            ("FOI Request Log, Second Half 2026", Document.Category.FOI, 2026),
            ("Service Directory and Hotlines 2026", Document.Category.OTHER, 2026),
            ("City Scholarship Guidelines 2026", Document.Category.OTHER, 2026),
        ]
        for _order, (title, category, year) in enumerate(samples, start=1):
            Document.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "category": category,
                    "year": year,
                    "description": "Prototype record. Replace with the signed PDF before launch.",
                    "external_url": "https://puertoprincesa.ph/",
                    "published_at": aware(date(year, 1, 15)),
                },
            )

    def seed_content(self):
        for item in prototype_data.NEWS_ARTICLES:
            Article.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "summary": item["summary"],
                    "body": "\n\n".join(item["body"]),
                    "category": Article.Category.NEWS,
                    "published_at": aware(item["date"]),
                },
            )

        for item in prototype_data.EVENTS:
            slug = slugify(item["title"])
            Event.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": item["title"],
                    "description": item.get("description", f"City event at {item['venue']}."),
                    "start_datetime": aware(item["date"], 8),
                    "end_datetime": aware(item["date"], 10),
                    "venue": item["venue"],
                },
            )

        for index, item in enumerate(prototype_data.NOTICES, start=1):
            Notice.objects.update_or_create(
                slug=slugify(item["title"]),
                defaults={
                    "title": item["title"],
                    "body": item.get("body", item["title"]),
                    "is_urgent": index == 1,
                    "published_at": timezone.now() - timedelta(days=index),
                },
            )

    def seed_complaints(self, agencies):
        now = timezone.now()
        subjects = [
            ("Broken street light", Complaint.Category.INFRASTRUCTURE),
            ("Uncollected garbage", Complaint.Category.SANITATION),
            ("Stray dogs near the public market", Complaint.Category.HEALTH),
            ("Illegal dumping along the highway", Complaint.Category.ENVIRONMENT),
            ("Flooded drainage after heavy rain", Complaint.Category.INFRASTRUCTURE),
            ("Senior citizen assistance follow-up", Complaint.Category.SOCIAL),
            ("Noisy videoke past midnight", Complaint.Category.SAFETY),
            ("Business permit renewal delay", Complaint.Category.BUSINESS),
            ("Fallen tree blocking a barangay road", Complaint.Category.SAFETY),
            ("Tour guide accreditation question", Complaint.Category.OTHER),
            ("Pothole on a school access road", Complaint.Category.INFRASTRUCTURE),
            ("Missed waste collection", Complaint.Category.SANITATION),
            ("Dengue hot spot near a canal", Complaint.Category.HEALTH),
            ("Smoke from open burning", Complaint.Category.ENVIRONMENT),
            ("Street vendor obstructing the sidewalk", Complaint.Category.SAFETY),
            ("Water bill adjustment request", Complaint.Category.BUSINESS),
            ("Tricycle fare overcharging", Complaint.Category.SAFETY),
            ("Assistance for a family in crisis", Complaint.Category.SOCIAL),
            ("Broken barangay health station door", Complaint.Category.HEALTH),
            ("Erosion along a coastal path", Complaint.Category.ENVIRONMENT),
            ("Unlit pedestrian crossing", Complaint.Category.INFRASTRUCTURE),
            ("Dead animal on the roadside", Complaint.Category.SANITATION),
            ("Request for a barangay day-care slot", Complaint.Category.SOCIAL),
            ("Permit requirements inquiry", Complaint.Category.BUSINESS),
        ]
        statuses = [
            Complaint.Status.RESOLVED,
            Complaint.Status.IN_REVIEW,
            Complaint.Status.RESOLVED,
            Complaint.Status.REFERRED,
            Complaint.Status.RECEIVED,
            Complaint.Status.CLOSED,
            Complaint.Status.RESOLVED,
            Complaint.Status.IN_REVIEW,
            Complaint.Status.RESOLVED,
            Complaint.Status.RECEIVED,
        ]
        details = [
            "Reported through the Sumbungan form with photos of the concern.",
            "Resident called the action line and followed up through the tracker.",
            "Raised during a barangay assembly and endorsed to the city government.",
            "Submitted online with a landmark to help the response team.",
        ]
        # Repeat the busier urban barangays so the dashboard's geographic chart
        # shows a realistic spread instead of one complaint in every barangay.
        demo_barangays = [
            "Bancao-bancao",
            "Bancao-bancao",
            "Bancao-bancao",
            "San Pedro",
            "San Pedro",
            "San Pedro",
            "San Jose",
            "San Jose",
            "Tiniguiban",
            "Tiniguiban",
            "Tiniguiban",
            "Sicsican",
            "Sicsican",
            "Irawan",
            "Irawan",
            "Manggahan",
            "Manggahan",
            "Tagburos",
            "San Miguel",
            "San Miguel",
            "Santa Monica",
            "Mandaragat",
            "Mandaragat",
            "Bagong Sikat",
            "San Manuel",
            "Luzviminda",
            "Buenavista",
            "Bacungan",
        ]

        # Remove only the demo complaints this command previously created, so
        # re-seeding stays idempotent without touching real submissions.
        Complaint.objects.filter(details__in=details).delete()

        for index in range(48):
            base, category = subjects[index % len(subjects)]
            barangay = demo_barangays[(index * 5) % len(demo_barangays)]
            subject = f"{base} in Barangay {barangay}"
            status = statuses[index % len(statuses)]
            days_ago = 2 + (index * 13) % 175
            created_at = now - timedelta(days=days_ago, hours=index % 9)
            agency = agencies.get(category)
            is_anonymous = index % 4 == 0

            complaint, _ = Complaint.objects.update_or_create(
                subject=subject,
                defaults={
                    "category": category,
                    "agency": agency,
                    "details": details[index % len(details)],
                    "barangay": barangay,
                    "landmark": "Near the barangay hall" if index % 3 == 0 else "",
                    "name": "" if is_anonymous else "Demo resident",
                    "email": "" if is_anonymous else "demo@example.com",
                    "phone": "" if is_anonymous else "09170000000",
                    "is_anonymous": is_anonymous,
                    "consent": True,
                },
            )

            resolution_days = min(2 + index % 6, max(days_ago - 0.25, 0.5))
            resolved_at = (
                created_at + timedelta(days=resolution_days)
                if status in {Complaint.Status.RESOLVED, Complaint.Status.CLOSED}
                else None
            )
            Complaint.objects.filter(pk=complaint.pk).update(
                created_at=created_at,
                status=status,
                resolved_at=resolved_at,
            )

            complaint.updates.all().delete()
            steps = [
                (
                    Complaint.Status.RECEIVED,
                    created_at,
                    "Concern received through the Sumbungan ng Bayan form.",
                )
            ]
            if status != Complaint.Status.RECEIVED:
                steps.append(
                    (
                        Complaint.Status.IN_REVIEW,
                        created_at + timedelta(hours=8),
                        "Triage team reviewed the report and checked the details.",
                    )
                )
            if status in {
                Complaint.Status.REFERRED,
                Complaint.Status.RESOLVED,
                Complaint.Status.CLOSED,
            }:
                steps.append(
                    (
                        Complaint.Status.REFERRED,
                        created_at + timedelta(days=1),
                        f"Referred to {agency.name if agency else 'the concerned office'}.",
                    )
                )
            if status in {Complaint.Status.RESOLVED, Complaint.Status.CLOSED}:
                steps.append(
                    (
                        Complaint.Status.RESOLVED,
                        resolved_at,
                        "Work completed and verified by the response team.",
                    )
                )
            if status == Complaint.Status.CLOSED:
                steps.append(
                    (
                        Complaint.Status.CLOSED,
                        resolved_at + timedelta(days=2),
                        "Resident confirmed the resolution. Request closed.",
                    )
                )

            for step_status, step_time, note in steps:
                update = ComplaintUpdate.objects.create(
                    complaint=complaint,
                    status=step_status,
                    note=note,
                )
                ComplaintUpdate.objects.filter(pk=update.pk).update(created_at=step_time)

    def seed_feedback(self):
        samples = [
            ("/", True, "Mabilis hanapin ang services."),
            ("/", True, "Malinaw ang layout at madaling basahin."),
            ("/", False, "Mas gusto ko sana ang mas malaking search box."),
            ("/directory/", True, "Complete ang contact details."),
            ("/directory/", True, "Nahanap ko agad ang hotline ng health office."),
            ("/directory/", False, "Kulang ang email ng isang opisina."),
            ("/search/", False, "Walang lumabas sa voice search ko."),
            ("/search/", True, "Mabilis ang results para sa business permit."),
            ("/sumbungan/", True, "Madaling sundan ang steps."),
            ("/sumbungan/", True, "Nakatanggap ako ng update sa tracker."),
            ("/sumbungan/", False, "Puwede bang mag-upload ng mas maraming photos?"),
            ("/tourism/", True, "Maganda ang photos at layout."),
            ("/tourism/", True, "Gusto ko ang festival calendar."),
            ("/tourism/", False, "Paki-add ang updated tour rates."),
            ("/accessibility/", True, "Malinaw ang accessibility statement."),
            ("/accessibility/", True, "Madaling mahanap ang contact para sa barrier."),
            ("/news/", False, "Puwede bang may filter by category?"),
            ("/news/", True, "Updated ang mga balita."),
            ("/news/", True, "Mas madaling basahin ang bagong cards."),
            ("/contact/", True, "Mabilis ang reply sa email."),
            ("/contact/", False, "Hindi ko makita ang office hours sa mobile."),
            ("/transparency/", True, "Nakita ko ang budget documents."),
            ("/transparency/", True, "Sana may CSV download din."),
            ("/faq/", True, "Nasagot ng chatbot ang tanong ko."),
            ("/faq/", True, "Malinaw ang mga sagot."),
            ("/faq/", False, "May tanong na wala sa listahan."),
            ("/emergency/", True, "Nandiyan lahat ng hotlines."),
            ("/emergency/", True, "Madaling i-copy ang numbers."),
            ("/government/", True, "Complete ang directory ng officials."),
            ("/about/", True, "Maganda ang history section."),
        ]
        now = timezone.now()
        for index, (page, helpful, comment) in enumerate(samples):
            feedback, _ = Feedback.objects.get_or_create(
                page=page, helpful=helpful, comment=comment
            )
            Feedback.objects.filter(pk=feedback.pk).update(
                created_at=now - timedelta(days=2 + (index * 5) % 170),
                is_reviewed=index % 4 == 0,
            )

    def seed_contact_messages(self):
        samples = [
            (
                "Maria Santos",
                "Business permit",
                "Good day, I would like to ask about the requirements for renewing a sari-sari store permit.",
            ),
            (
                "Jose Dela Cruz",
                "Road concern",
                "May malaking lubak po sa kalsada papasok sa aming barangay. Sana po maaksyunan.",
            ),
            (
                "Ana Reyes",
                "Tourism",
                "Do you have updated schedules for the Underground River tours this December?",
            ),
            (
                "Mark Villanueva",
                "Scholarship",
                "When will the city scholarship results be released?",
            ),
            ("Liza Fernandez", "Health services", "Is the mental health clinic open on Saturdays?"),
            (
                "Ramon Garcia",
                "Waste collection",
                "Our street was not included in the garbage collection route this week.",
            ),
            (
                "Grace Lim",
                "Senior citizen ID",
                "What documents should my mother bring for her senior citizen ID renewal?",
            ),
            (
                "Paolo Mendoza",
                "Events",
                "We would like to invite the city to our school's cultural festival.",
            ),
            (
                "Carla Bautista",
                "Employment",
                "Are there job openings for PESO registrants this month?",
            ),
            (
                "Noel Aquino",
                "Tax payment",
                "Can I pay my business tax online or do I need to go to the office?",
            ),
            (
                "Jenny Tan",
                "FOI",
                "I submitted an FOI request last week and would like to follow up.",
            ),
            (
                "Victor Ramos",
                "Emergency",
                "Please update the hotline number for the rescue team in our area.",
            ),
            (
                "Elena Cruz",
                "Housing",
                "Where can I inquire about the city's housing assistance program?",
            ),
            ("Dennis Reyes", "Sports", "How can our barangay join the youth sports festival?"),
            (
                "Mia Gonzales",
                "Website",
                "The directory page is very helpful. Thank you for the update.",
            ),
        ]
        now = timezone.now()
        for index, (name, topic, message) in enumerate(samples):
            contact, _ = ContactMessage.objects.get_or_create(
                name=name,
                topic=topic,
                message=message,
                defaults={
                    "email": f"{name.split()[0].lower()}@example.com",
                    "phone": "09170000000" if index % 3 == 0 else "",
                    "consent": True,
                },
            )
            ContactMessage.objects.filter(pk=contact.pk).update(
                created_at=now - timedelta(days=1 + (index * 9) % 160),
                is_reviewed=index % 5 == 0,
            )

    def seed_users(self):
        User = get_user_model()
        staff, created = User.objects.get_or_create(
            username="staff",
            defaults={
                "email": "staff@example.com",
                "is_staff": True,
                "first_name": "City",
                "last_name": "Staff",
            },
        )
        if created:
            staff.set_password("prototype-staff-2026")
            staff.save()
        # Give the demo staff account view/add/change rights on content so the
        # "Open in content admin" links in the dashboard work out of the box.
        # Delete stays with the superuser.
        staff.user_permissions.set(
            Permission.objects.filter(
                content_type__app_label="content",
            ).exclude(codename__startswith="delete_")
        )
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
                "first_name": "City",
                "last_name": "Admin",
            },
        )
        if created:
            admin.set_password("prototype-admin-2026")
            admin.save()
        self.stdout.write("Demo users: staff / prototype-staff-2026, admin / prototype-admin-2026")
