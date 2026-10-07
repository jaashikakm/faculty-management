from django.urls import path
from .views import dashboard, faculty_list

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("faculty/", faculty_list, name="faculty_list"),
]
