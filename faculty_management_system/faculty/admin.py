from django.contrib import admin
from .models import Department, FacultyProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ("faculty_id", "full_name", "department", "designation", "date_of_joining")
    list_filter = ("department", "designation", "is_active_faculty")
    search_fields = ("faculty_id", "user__first_name", "user__last_name")
