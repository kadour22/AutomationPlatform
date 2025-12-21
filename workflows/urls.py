from django.urls import path
from . import views

urlpatterns = [
    path('workflows-lists/', views.workflow_api_list.as_view()),
    path('workflow/<int:workflow_id>/workflow-detail', views.workflow_by_ID.as_view()),
] 