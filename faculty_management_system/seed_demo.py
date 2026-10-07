import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faculty_management.settings")
django.setup()

from django.contrib.auth.models import User, Group
from faculty.models import Department, FacultyProfile

dept, _ = Department.objects.get_or_create(code="AIDS", defaults={"name": "Artificial Intelligence and Data Science"})
user, created = User.objects.get_or_create(username="faculty01", defaults={
    "first_name": "Jaashika", "last_name": "KM", "email": "faculty@example.com"
})
if created:
    user.set_password("Faculty@123")
    user.save()

group, _ = Group.objects.get_or_create(name="Faculty")
user.groups.add(group)

FacultyProfile.objects.get_or_create(
    user=user,
    defaults={
        "faculty_id": "FAC001",
        "department": dept,
        "designation": "AP",
        "mobile": "9999999999",
        "date_of_birth": "1998-01-15",
        "date_of_joining": "2022-06-01",
    }
)
print("Demo faculty created: faculty01 / Faculty@123")
