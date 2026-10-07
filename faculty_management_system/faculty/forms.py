from django import forms
from .models import FacultyProfile

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = [
            "faculty_id", "department", "designation", "mobile",
            "date_of_birth", "date_of_joining", "profile_photo"
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_of_joining": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
