from django.conf import settings
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class FacultyProfile(models.Model):
    DESIGNATIONS = [
        ("AP", "Assistant Professor"),
        ("AP_SG", "Assistant Professor (Senior Grade)"),
        ("ASP", "Associate Professor"),
        ("PROF", "Professor"),
        ("HOD", "Head of Department"),
        ("DEAN", "Dean"),
        ("DIRECTOR", "Director"),
        ("PRINCIPAL", "Principal"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    designation = models.CharField(max_length=20, choices=DESIGNATIONS)
    mobile = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_active_faculty = models.BooleanField(default=True)

    class Meta:
        ordering = ["faculty_id"]

    def __str__(self):
        return f"{self.faculty_id} - {self.user.get_full_name() or self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
