from django.conf import settings
from django.db import models
from faculty.models import FacultyProfile

class Task(models.Model):
    PRIORITIES = [
        ("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High"), ("URGENT", "Urgent")
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES, default="MEDIUM")
    due_date = models.DateField()
    attachment = models.FileField(upload_to="task_attachments/", blank=True, null=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskAssignment(models.Model):
    STATUS = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name="task_assignments")
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    remarks = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["task", "faculty"], name="unique_task_faculty")
        ]
