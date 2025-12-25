from django.urls import path
from . import views


urlpatterns = [
    path('tasks-list/', views.tasks_lists_view.as_view(), name='tasks-list'),
    path('create/', views.create_task_view.as_view(), name='tasks-create'),
    path('task/<int:task_id>/delete', views.delete_task_view.as_view(), name='tasks-delete'),
]