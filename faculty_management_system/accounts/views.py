from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm

class FacultyLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect("dashboard")
