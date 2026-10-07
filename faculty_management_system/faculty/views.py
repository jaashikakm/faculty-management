from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import FacultyProfile
from leave_management.models import LeaveApplication
from task_management.models import Task, TaskAssignment
from circulars.models import Circular

def _profile(request):
    return getattr(request.user, "facultyprofile", None)

def _is_admin_role(user):
    return user.is_superuser or user.groups.filter(
        name__in=["HOD", "Dean", "Director", "Principal"]
    ).exists()

@login_required
def dashboard(request):
    profile = _profile(request)
    today = date.today()

    birthdays = FacultyProfile.objects.filter(
        is_active_faculty=True,
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    ).select_related("user", "department")

    anniversaries = FacultyProfile.objects.filter(
        is_active_faculty=True,
        date_of_joining__month=today.month,
        date_of_joining__day=today.day
    ).select_related("user", "department")

    if profile:
        pending_leaves = LeaveApplication.objects.filter(
            faculty=profile, status="PENDING"
        ).count()
        my_tasks = TaskAssignment.objects.filter(
            faculty=profile, status__in=["PENDING", "IN_PROGRESS"]
        ).select_related("task")
    else:
        pending_leaves = 0
        my_tasks = TaskAssignment.objects.none()

    if _is_admin_role(request.user):
        leave_requests = LeaveApplication.objects.filter(
            status="PENDING"
        ).select_related("faculty__user", "faculty__department")[:10]
        tasks = Task.objects.all().order_by("-created_at")[:10]
    else:
        leave_requests = LeaveApplication.objects.none()
        tasks = Task.objects.none()

    circulars = Circular.objects.filter(is_published=True).order_by("-published_at")[:5]

    return render(request, "faculty/dashboard.html", {
        "profile": profile,
        "birthdays": birthdays,
        "anniversaries": anniversaries,
        "pending_leaves": pending_leaves,
        "my_tasks": my_tasks,
        "leave_requests": leave_requests,
        "tasks": tasks,
        "circulars": circulars,
        "is_admin_role": _is_admin_role(request.user),
    })

@login_required
def faculty_list(request):
    if not _is_admin_role(request.user):
        messages.error(request, "You do not have permission to view all faculty.")
        return redirect("dashboard")
    qs = FacultyProfile.objects.select_related("user", "department").all()
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(faculty_id__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(department__name__icontains=q)
        )
    return render(request, "faculty/faculty_list.html", {"faculty": qs, "q": q})
