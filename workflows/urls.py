from django.urls import path
from . import views

urlpatterns = [
    # workflows urls
    path('workflows-lists/', views.workflow_api_list.as_view()),
    path('workflow/<int:workflow_id>/workflow-detail', views.workflow_by_ID.as_view()),
    path('workflow/<int:workflow_id>/workflow-delete', views.delete_workflow_view.as_view()),
    # workflows steps urls
    path('workflow-step-create/' , views.create_workflow_steps_view.as_view())
] 