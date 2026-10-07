from django.urls import path
from .views import create_task, task_list, update_task_status

urlpatterns = [
    path("", task_list, name="task_list"),
    path("create/", create_task, name="create_task"),
    path("assignment/<int:assignment_id>/update/", update_task_status, name="update_task_status"),
]
