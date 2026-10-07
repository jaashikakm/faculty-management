from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from faculty.models import FacultyProfile
from .forms import LeaveApplicationForm
from .models import LeaveApplication, LeaveStatus
from .services import leave_balance

ADMIN_GROUPS = ["HOD", "Dean", "Director", "Principal"]

def is_leave_admin(user):
    return user.is_superuser or user.groups.filter(name__in=ADMIN_GROUPS).exists()

def get_profile(user):
    return getattr(user, "facultyprofile", None)

@login_required
def apply_leave(request):
    profile = get_profile(request.user)
    if not profile:
        messages.error(request, "Your faculty profile is not configured.")
        return redirect("dashboard")

    if request.method == "POST":
        form = LeaveApplicationForm(request.POST, request.FILES, initial={"faculty": profile})
        if form.is_valid():
            obj = form.save(commit=False)
            obj.faculty = profile
            obj.status = LeaveStatus.PENDING
            obj.save()
            messages.success(request, "Leave application submitted successfully.")
            return redirect("my_leaves")
    else:
        form = LeaveApplicationForm(initial={"faculty": profile})

    return render(request, "leave/apply_leave.html", {
        "form": form,
        "profile": profile,
    })

@login_required
def my_leaves(request):
    profile = get_profile(request.user)
    leaves = LeaveApplication.objects.filter(faculty=profile) if profile else LeaveApplication.objects.none()
    return render(request, "leave/my_leaves.html", {"leaves": leaves})

@login_required
def leave_balance_view(request):
    profile = get_profile(request.user)
    balances = {}
    if profile:
        from .models import LeaveType
        for leave_type in [LeaveType.CL, LeaveType.PERMISSION, LeaveType.EL, LeaveType.ML]:
            balances[leave_type.label] = leave_balance(profile, leave_type)
    return render(request, "leave/leave_balance.html", {"balances": balances})

@login_required
def pending_leaves(request):
    if not is_leave_admin(request.user):
        messages.error(request, "You do not have permission to approve leave.")
        return redirect("dashboard")
    leaves = LeaveApplication.objects.filter(
        status=LeaveStatus.PENDING
    ).select_related("faculty__user", "faculty__department")
    return render(request, "leave/pending_leaves.html", {"leaves": leaves})

@require_POST
@login_required
@transaction.atomic
def approve_leave(request, pk):
    if not is_leave_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect("dashboard")
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if leave.status != LeaveStatus.PENDING:
        messages.warning(request, "This application has already been processed.")
        return redirect("pending_leaves")
    leave.status = LeaveStatus.APPROVED
    leave.approved_by = request.user
    leave.approval_remarks = request.POST.get("remarks", "")
    leave.save(update_fields=["status", "approved_by", "approval_remarks"])
    messages.success(request, "Leave approved.")
    return redirect("pending_leaves")

@require_POST
@login_required
def reject_leave(request, pk):
    if not is_leave_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect("dashboard")
    leave = get_object_or_404(LeaveApplication, pk=pk)
    leave.status = LeaveStatus.REJECTED
    leave.approved_by = request.user
    leave.approval_remarks = request.POST.get("remarks", "")
    leave.save(update_fields=["status", "approved_by", "approval_remarks"])
    messages.success(request, "Leave rejected.")
    return redirect("pending_leaves")
