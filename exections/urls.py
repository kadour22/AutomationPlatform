from django.urls import path
from . import views

urlpatterns = [
    path("execute-workflow/" , views.WorkflowExecutionView.as_view())
]

