from django.contrib import admin
from .models import LeaveApplication

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ("faculty", "leave_type", "from_date", "to_date", "permission_hours", "status", "applied_at")
    list_filter = ("leave_type", "status")
    search_fields = ("faculty__faculty_id", "faculty__user__first_name", "faculty__user__last_name")
