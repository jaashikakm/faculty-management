from django.urls import path
from .views import circular_list, create_circular

urlpatterns = [
    path("", circular_list, name="circular_list"),
    path("create/", create_circular, name="create_circular"),
]
