from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from faculty.models import FacultyProfile
from .forms import TaskForm
from .models import Task, TaskAssignment

ADMIN_GROUPS = ["HOD", "Dean", "Director", "Principal"]

def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=ADMIN_GROUPS).exists()

@login_required
def create_task(request):
    if not is_admin(request.user):
        messages.error(request, "Only HOD, Dean, Director or Principal can assign tasks.")
        return redirect("dashboard")

    faculty = FacultyProfile.objects.filter(is_active_faculty=True).select_related("user", "department")
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        selected = request.POST.getlist("faculty_ids")
        if form.is_valid():
            if not selected:
                form.add_error(None, "Select at least one faculty member.")
            else:
                task = form.save(commit=False)
                task.assigned_by = request.user
                task.save()
                TaskAssignment.objects.bulk_create([
                    TaskAssignment(task=task, faculty_id=fid) for fid in selected
                ])
                messages.success(request, "Task assigned successfully.")
                return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form, "faculty": faculty})

@login_required
def task_list(request):
    profile = getattr(request.user, "facultyprofile", None)
    if is_admin(request.user):
        tasks = Task.objects.select_related("assigned_by").prefetch_related("assignments__faculty__user").order_by("-created_at")
    elif profile:
        tasks = Task.objects.filter(assignments__faculty=profile).distinct().order_by("-created_at")
    else:
        tasks = Task.objects.none()
    return render(request, "tasks/task_list.html", {"tasks": tasks, "is_admin": is_admin(request.user)})

@login_required
def update_task_status(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, pk=assignment_id)
    profile = getattr(request.user, "facultyprofile", None)
    if profile != assignment.faculty and not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect("task_list")
    if request.method == "POST":
        assignment.status = request.POST.get("status", assignment.status)
        assignment.remarks = request.POST.get("remarks", "")
        assignment.save()
        messages.success(request, "Task status updated.")
    return redirect("task_list")
