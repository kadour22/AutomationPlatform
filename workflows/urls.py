from django.urls import path
from . import views

urlpatterns = [
    path('workflows-lists/', views.workflow_api_list.as_view()),
] 