from django.urls import path
from .views import (
    apply_leave, my_leaves, leave_balance_view,
    pending_leaves, approve_leave, reject_leave
)

urlpatterns = [
    path("apply/", apply_leave, name="apply_leave"),
    path("mine/", my_leaves, name="my_leaves"),
    path("balance/", leave_balance_view, name="leave_balance"),
    path("pending/", pending_leaves, name="pending_leaves"),
    path("<int:pk>/approve/", approve_leave, name="approve_leave"),
    path("<int:pk>/reject/", reject_leave, name="reject_leave"),
]
