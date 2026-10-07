from django import forms
from .models import LeaveApplication, LeaveType
from .services import validate_leave_request

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ["leave_type", "from_date", "to_date", "permission_hours", "reason", "attachment"]
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "to_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "permission_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.5", "min": "0", "max": "1"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "leave_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            return cleaned
        leave_type = cleaned.get("leave_type")
        start = cleaned.get("from_date")
        end = cleaned.get("to_date")
        permission_hours = cleaned.get("permission_hours") or 0
        if leave_type and start and end:
            # faculty is injected by the view
            faculty = self.initial.get("faculty")
            if faculty:
                ok, message = validate_leave_request(
                    faculty, leave_type, start, end, permission_hours
                )
                if not ok:
                    raise forms.ValidationError(message)
        return cleaned
