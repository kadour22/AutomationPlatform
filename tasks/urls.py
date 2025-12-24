from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.tasks_view_logic.as_view(), name='tasks-list-create'),
    path('tasks/<int:task_id>/', views.tasks_view_logic.as_view(), name='tasks-delete'),
]