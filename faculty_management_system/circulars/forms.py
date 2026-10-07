from django import forms
from .models import Circular

class CircularForm(forms.ModelForm):
    class Meta:
        model = Circular
        fields = ["circular_number", "subject", "content", "attachment", "is_published"]
        widgets = {
            "circular_number": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 7}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
