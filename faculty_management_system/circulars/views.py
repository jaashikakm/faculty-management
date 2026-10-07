from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CircularForm
from .models import Circular

ADMIN_GROUPS = ["HOD", "Dean", "Director", "Principal"]

def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=ADMIN_GROUPS).exists()

@login_required
def circular_list(request):
    circulars = Circular.objects.filter(is_published=True)
    return render(request, "circulars/circular_list.html", {"circulars": circulars})

@login_required
def create_circular(request):
    if not is_admin(request.user):
        messages.error(request, "Only HOD, Dean, Director or Principal can create circulars.")
        return redirect("circular_list")
    if request.method == "POST":
        form = CircularForm(request.POST, request.FILES)
        if form.is_valid():
            circular = form.save(commit=False)
            circular.created_by = request.user
            circular.save()
            messages.success(request, "Circular published successfully.")
            return redirect("circular_list")
    else:
        form = CircularForm()
    return render(request, "circulars/create_circular.html", {"form": form})
