"""Staff-only dashboard: KPIs, charts, complaint triage, and feedback.

The dashboard reads from the same models as the public site. Every number on
the page comes from an ORM query, so the prototype stays data-driven: edit a
complaint in Django admin and the charts change on the next request.
"""

import csv
from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from content.constants import BARANGAYS
from content.models import (
    Agency,
    Article,
    Complaint,
    ComplaintUpdate,
    Document,
    Event,
    Feedback,
    Notice,
    Office,
    Service,
)


def staff_required(view):
    """Authenticated staff only; everyone else gets a clear 403."""

    @login_required
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("The dashboard is for city staff and administrators.")
        return view(request, *args, **kwargs)

    return wrapped


STATUS_COLORS = {
    Complaint.Status.RECEIVED: "#0b3f91",
    Complaint.Status.IN_REVIEW: "#e0ae00",
    Complaint.Status.REFERRED: "#2f7ae5",
    Complaint.Status.RESOLVED: "#1f7a4d",
    Complaint.Status.CLOSED: "#6f84a1",
}


def add_months(day, months):
    month = day.month - 1 + months
    year = day.year + month // 12
    month = month % 12 + 1
    return day.replace(year=year, month=month, day=1)


def percent(value, total):
    return round((value / total) * 100, 1) if total else 0


@staff_required
def overview(request):
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    complaints = Complaint.objects.all()

    total = complaints.count()
    open_count = complaints.exclude(
        status__in=[Complaint.Status.RESOLVED, Complaint.Status.CLOSED]
    ).count()
    resolved_count = complaints.filter(status=Complaint.Status.RESOLVED).count()
    new_this_month = complaints.filter(created_at__gte=month_start).count()

    resolved = [
        item
        for item in complaints.filter(resolved_at__isnull=False).only("created_at", "resolved_at")
        if item.resolved_at
    ]
    durations = [(item.resolved_at - item.created_at).total_seconds() / 86400 for item in resolved]
    avg_resolution = round(sum(durations) / len(durations), 1) if durations else None

    # Complaints per agency.
    agency_rows = []
    for row in complaints.values("agency__name").annotate(total=Count("id")).order_by("-total")[:8]:
        agency_rows.append(
            {
                "label": row["agency__name"] or "Unassigned",
                "value": row["total"],
                "percent": percent(row["total"], total),
            }
        )

    # Status split + a CSS conic-gradient donut.
    status_rows = []
    for value, label in Complaint.Status.choices:
        count = complaints.filter(status=value).count()
        status_rows.append(
            {
                "value": value,
                "label": label,
                "count": count,
                "percent": percent(count, total),
                "color": STATUS_COLORS[value],
            }
        )
    stops = []
    cursor = 0
    for row in status_rows:
        if row["percent"]:
            start = cursor
            cursor += row["percent"]
            stops.append(f"{row['color']} {start}% {cursor}%")
    donut_gradient = (
        "conic-gradient(" + ", ".join(stops) + ")" if stops else "conic-gradient(#e0eaf7 0% 100%)"
    )

    # Six-month trend + SVG line coordinates.
    start_month = add_months(month_start, -5)
    counts = {
        row["month"].strftime("%Y-%m"): row["total"]
        for row in complaints.filter(created_at__gte=start_month)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
    }
    trend = []
    for offset in range(6):
        bucket = add_months(start_month, offset)
        trend.append(
            {
                "label": bucket.strftime("%b"),
                "value": counts.get(bucket.strftime("%Y-%m"), 0),
            }
        )
    peak = max((item["value"] for item in trend), default=0) or 1
    chart_width, chart_height, pad = 620, 190, 26
    step = (chart_width - pad * 2) / max(len(trend) - 1, 1)
    points = []
    dots = []
    for index, item in enumerate(trend):
        x = round(pad + index * step, 1)
        y = round(chart_height - pad - (item["value"] / peak) * (chart_height - pad * 2), 1)
        points.append(f"{x},{y}")
        dots.append({"x": x, "y": y, **item})
    trend_points = " ".join(points)

    # Top categories.
    category_labels = dict(Complaint.Category.choices)
    category_rows = [
        {
            "label": category_labels.get(row["category"], row["category"]),
            "value": row["total"],
            "percent": percent(row["total"], total),
        }
        for row in complaints.values("category").annotate(total=Count("id")).order_by("-total")[:5]
    ]

    # Top barangays: gives the desk a geographic view of the caseload.
    barangay_rows = [
        {
            "label": row["barangay"] or "Not specified",
            "value": row["total"],
            "percent": percent(row["total"], total),
        }
        for row in complaints.exclude(barangay="")
        .values("barangay")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    ]

    feedback_total = Feedback.objects.count()
    feedback_unreviewed = Feedback.objects.filter(is_reviewed=False).count()
    feedback_helpful = Feedback.objects.filter(helpful=True).count()
    feedback_rows = [
        {
            "label": "Helpful",
            "count": feedback_helpful,
            "percent": percent(feedback_helpful, feedback_total),
            "color": "#1f7a4d",
        },
        {
            "label": "Not helpful",
            "count": feedback_total - feedback_helpful,
            "percent": percent(feedback_total - feedback_helpful, feedback_total),
            "color": "#e0ae00",
        },
    ]
    feedback_stops = []
    feedback_cursor = 0
    for row in feedback_rows:
        if row["percent"]:
            feedback_stops.append(
                f"{row['color']} {feedback_cursor}% {feedback_cursor + row['percent']}%"
            )
            feedback_cursor += row["percent"]
    feedback_gradient = (
        "conic-gradient(" + ", ".join(feedback_stops) + ")"
        if feedback_stops
        else "conic-gradient(#e0eaf7 0% 100%)"
    )

    content_counts = {
        "Articles": Article.objects.count(),
        "Upcoming events": Event.objects.filter(start_datetime__gte=now).count(),
        "Notices": Notice.objects.count(),
        "Services": Service.objects.count(),
        "Offices": Office.objects.count(),
        "Documents": Document.objects.count(),
    }

    context = {
        "total_complaints": total,
        "kpis": [
            {
                "label": "Open complaints",
                "value": open_count,
                "hint": f"{total} total received",
                "tone": "primary",
            },
            {
                "label": "New this month",
                "value": new_this_month,
                "hint": month_start.strftime("%B %Y"),
                "tone": "accent",
            },
            {
                "label": "Resolved",
                "value": resolved_count,
                "hint": "Closed loop with the resident",
                "tone": "success",
            },
            {
                "label": "Avg. resolution",
                "value": f"{avg_resolution} days" if avg_resolution is not None else "—",
                "hint": "From received to resolved",
                "tone": "secondary",
            },
        ],
        "agency_rows": agency_rows,
        "status_rows": status_rows,
        "donut_gradient": donut_gradient,
        "trend": trend,
        "trend_points": trend_points,
        "trend_dots": dots,
        "chart_width": chart_width,
        "chart_height": chart_height,
        "category_rows": category_rows,
        "barangay_rows": barangay_rows,
        "feedback_total": feedback_total,
        "feedback_unreviewed": feedback_unreviewed,
        "feedback_helpful": feedback_helpful,
        "feedback_rows": feedback_rows,
        "feedback_gradient": feedback_gradient,
        "content_counts": content_counts,
        "recent_complaints": complaints.select_related("agency")[:8],
    }
    return render(request, "dashboard/overview.html", context)


def _parse_day(value):
    """Parse an ISO date from a query string, or return ``None``."""
    try:
        return date.fromisoformat((value or "").strip())
    except ValueError:
        return None


def _date_filter(queryset, request):
    """Apply the dashboard's shared ``from``/``to`` date range.

    Both ends are inclusive and compare on the calendar date, so a resident's
    request sent late in the evening still lands on the day staff expect.
    Invalid values are ignored rather than raising a 500.
    """
    start = _parse_day(request.GET.get("from"))
    end = _parse_day(request.GET.get("to"))
    if start:
        queryset = queryset.filter(created_at__date__gte=start)
    if end:
        queryset = queryset.filter(created_at__date__lte=end)
    return queryset, start, end


def _complaint_queryset(request):
    """Complaints matching the desk filters; shared by the list and the export."""
    queryset = Complaint.objects.select_related("agency", "assigned_to")
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()
    agency = request.GET.get("agency", "").strip()
    barangay = request.GET.get("barangay", "").strip()

    if query:
        queryset = queryset.filter(
            Q(reference__icontains=query)
            | Q(subject__icontains=query)
            | Q(details__icontains=query)
            | Q(name__icontains=query)
            | Q(barangay__icontains=query)
            | Q(landmark__icontains=query)
        )
    if status:
        queryset = queryset.filter(status=status)
    if category:
        queryset = queryset.filter(category=category)
    if agency:
        queryset = queryset.filter(agency_id=agency)
    if barangay:
        queryset = queryset.filter(barangay=barangay)

    queryset, date_from, date_to = _date_filter(queryset, request)
    return queryset, {
        "query": query,
        "status": status,
        "category": category,
        "agency": agency,
        "barangay": barangay,
        "date_from": date_from.isoformat() if date_from else "",
        "date_to": date_to.isoformat() if date_to else "",
    }


def _feedback_queryset(request):
    """Feedback matching the dashboard filters; shared by the list and export."""
    queryset = Feedback.objects.all()
    helpful = request.GET.get("helpful", "").strip()
    reviewed = request.GET.get("reviewed", "").strip()
    if helpful in {"1", "0"}:
        queryset = queryset.filter(helpful=helpful == "1")
    if reviewed in {"1", "0"}:
        queryset = queryset.filter(is_reviewed=reviewed == "1")

    queryset, date_from, date_to = _date_filter(queryset, request)
    return queryset, {
        "helpful": helpful,
        "reviewed": reviewed,
        "date_from": date_from.isoformat() if date_from else "",
        "date_to": date_to.isoformat() if date_to else "",
    }


@staff_required
def complaint_list(request):
    queryset, filters = _complaint_queryset(request)

    params = request.GET.copy()
    params.pop("page", None)
    querystring = params.urlencode()

    page = Paginator(queryset, 12).get_page(request.GET.get("page"))
    context = {
        "page_obj": page,
        "total": queryset.count(),
        **filters,
        "querystring": querystring,
        "statuses": Complaint.Status.choices,
        "categories": Complaint.Category.choices,
        "agencies": Agency.objects.all(),
        "barangays": BARANGAYS,
    }
    return render(request, "dashboard/complaints.html", context)


@staff_required
def export_complaints(request):
    """Download the current complaint view as a spreadsheet-friendly CSV."""
    queryset, filters = _complaint_queryset(request)
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="complaints-{timezone.localdate().isoformat()}.csv"'
    )
    # The BOM keeps Excel from mangling names with accents.
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(
        [
            "Reference",
            "Received",
            "Subject",
            "Category",
            "Barangay",
            "Landmark",
            "Agency",
            "Assigned to",
            "Status",
            "Overdue",
            "Resolved",
            "Name",
            "Email",
            "Phone",
        ]
    )
    for item in queryset.iterator():
        writer.writerow(
            [
                item.reference,
                timezone.localtime(item.created_at).strftime("%Y-%m-%d %H:%M"),
                item.subject,
                item.get_category_display(),
                item.barangay,
                item.landmark,
                item.agency.name if item.agency else "",
                item.assigned_to.get_username() if item.assigned_to else "",
                item.get_status_display(),
                "yes" if item.is_overdue else "no",
                timezone.localtime(item.resolved_at).strftime("%Y-%m-%d %H:%M")
                if item.resolved_at
                else "",
                item.name,
                item.email,
                item.phone,
            ]
        )
    return response


@staff_required
def complaint_detail(request, reference):
    complaint = get_object_or_404(
        Complaint.objects.select_related("agency", "assigned_to"),
        reference=reference,
    )
    if request.method == "POST":
        status = request.POST.get("status", "").strip()
        note = request.POST.get("note", "").strip()
        assigned_raw = request.POST.get("assigned_to", "").strip()
        is_public = request.POST.get("is_public") == "on"

        if status not in dict(Complaint.Status.choices):
            messages.error(request, "Choose a valid status.")
        else:
            previous_status = complaint.status
            complaint.status = status
            complaint.resolved_at = (
                timezone.now()
                if status in {Complaint.Status.RESOLVED, Complaint.Status.CLOSED}
                else None
            )
            if assigned_raw:
                complaint.assigned_to = (
                    get_user_model().objects.filter(pk=assigned_raw, is_staff=True).first()
                )
            else:
                complaint.assigned_to = None
            complaint.save()

            if status != previous_status or note:
                ComplaintUpdate.objects.create(
                    complaint=complaint,
                    status=status,
                    note=note,
                    is_public=is_public,
                    created_by=request.user,
                )
            messages.success(
                request,
                f"{complaint.reference} is now “{dict(Complaint.Status.choices)[status]}”.",
            )
            return redirect("dashboard:complaint_detail", reference=complaint.reference)

    context = {
        "complaint": complaint,
        "updates": complaint.updates.select_related("created_by"),
        "attachments": complaint.attachments.all(),
        "statuses": Complaint.Status.choices,
        "staff_users": get_user_model().objects.filter(is_staff=True, is_active=True),
    }
    return render(request, "dashboard/complaint_detail.html", context)


@staff_required
def feedback_list(request):
    queryset, filters = _feedback_queryset(request)

    params = request.GET.copy()
    params.pop("page", None)
    page = Paginator(queryset, 20).get_page(request.GET.get("page"))
    context = {
        "page_obj": page,
        "total": queryset.count(),
        **filters,
        "querystring": params.urlencode(),
        "positive": Feedback.objects.filter(helpful=True).count(),
        "negative": Feedback.objects.filter(helpful=False).count(),
    }
    return render(request, "dashboard/feedback.html", context)


@staff_required
def export_feedback(request):
    """Download the current feedback view as a spreadsheet-friendly CSV."""
    queryset, _filters = _feedback_queryset(request)
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="feedback-{timezone.localdate().isoformat()}.csv"'
    )
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(["Received", "Page", "Helpful", "Comment", "Reviewed"])
    for item in queryset.iterator():
        writer.writerow(
            [
                timezone.localtime(item.created_at).strftime("%Y-%m-%d %H:%M"),
                item.page,
                "yes" if item.helpful else "no",
                item.comment,
                "yes" if item.is_reviewed else "no",
            ]
        )
    return response
