from datetime import date
from decimal import Decimal
from django.conf import settings
from django.db import models

from faculty.models import FacultyProfile

class LeaveType(models.TextChoices):
    CL = "CL", "Casual Leave"
    PERMISSION = "PERMISSION", "Permission"
    EL = "EL", "Earned Leave"
    ML = "ML", "Medical Leave"

class LeaveStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"

class LeaveApplication(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name="leave_applications")
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    from_date = models.DateField()
    to_date = models.DateField()
    permission_hours = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("0.0"))
    reason = models.TextField()
    attachment = models.FileField(upload_to="leave_documents/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="approved_leaves"
    )
    approval_remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-applied_at"]

    @property
    def number_of_days(self):
        if self.leave_type == LeaveType.PERMISSION:
            return Decimal("0")
        return Decimal((self.to_date - self.from_date).days + 1)

    def __str__(self):
        return f"{self.faculty} - {self.get_leave_type_display()} - {self.status}"
