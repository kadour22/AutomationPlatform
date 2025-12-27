from django.urls import path
from . import views

urlpatterns = [
    path("approvals/", views.approvals_list, name="approvals_list"),
    path("approvals/<int:approval_id>/", views.approval_detail, name="approval_detail"),
]