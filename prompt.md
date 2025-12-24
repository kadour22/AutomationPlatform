so u are an expert in react js working in big company and ur manager give give this code and ask u to create a react js project that
handle everything in this backend code use tailwind and framer motions for desgin the porject idea is an Automationplatform 
u have 3 django apps : ur role is develope app and handle all logic from first time no issues and in the end u will find a db 

1 - workflow :
<!-- views file -->
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from workflows.models import WorkFlowStep
from workflows.serializers import workflow_steps_serializer
from workflows.services.workflow_services import (
    workflow_list , get_workflow_by_id , delete_workflow
)

from workflows.services.workflow_steps import create_workflow_steps

from .permmsions import IsOwnerPermission , ManagerPermission 

class workflow_api_list(APIView) :
    permission_class = [IsOwnerPermission]
    def get(self, request) :
        return workflow_list()

class workflow_by_ID(APIView) :
    permission_class = [IsOwnerPermission]
    def get(self, request, workflow_id) :
        return get_workflow_by_id(workflow_id=workflow_id)
    
class delete_workflow_view(APIView) :
    permission_class = [IsOwnerPermission]
    def delete(self, request , workflow_id) :
        return delete_workflow(workflow_id=workflow_id)
    
class create_workflow_steps_view(APIView) :
    permission_class = [IsOwnerPermission | ManagerPermission]
    def post(self, request) :
        return create_workflow_steps(data=request.data)

<!-- CRUD Logic -->
from workflows.models import WorkFlow
from workflows.serializers import workflow_serializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

def workflow_list() :
    workflows  = WorkFlow.objects.select_related("created_by").all()
    serializer = workflow_serializer(
        workflows , many=True
    ) 
    return Response(serializer.data , status=200)

def get_workflow_by_id(workflow_id) :
    workflow = get_object_or_404(WorkFlow , id=workflow_id)
    serializer = workflow_serializer(workflow)
    return Response(serializer.data , status=200)

def delete_workflow(workflow_id) :
    workflow = get_object_or_404(WorkFlow , id=workflow_id)
    workflow.delete()
    return Response("workflow deleted" , status=200)
<!-- urls -->
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

2 - executions app 
<!-- views file -->
from .serializers import WorkflowExecutionSerializer , StepExecution
from .models import WorkflowExecution
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .services.workflows_executions import(
    email_workflow_execuction , approval_workflow_execuction ,
    webhook_workflow_execuction , task_workflow_execuction
)

class WorkflowExecutionView(CreateModelMixin, GenericAPIView):
    serializer_class = WorkflowExecutionSerializer

    def post(self, request):
        print(request.user.email)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = serializer.validated_data["workflow"]
        triggered_by = serializer.validated_data.get("triggered_by")

        execution = WorkflowExecution.objects.create(
            workflow=workflow,
            triggered_by=triggered_by,
            status="running",
            context={}, 
            )

        execution.initialize_context(
            inputs={
                "user_id": triggered_by.id if triggered_by else None,
                "workflow_id": workflow.id,
            },
            metadata={
                "executed_by": triggered_by.username if triggered_by else "system",
                "workflow_name": workflow.name,
            }
        )

        first_step = workflow.steps.first()
        if not first_step:
            return Response(
                {"detail": "Workflow has no steps."},
                status=status.HTTP_400_BAD_REQUEST
            )

        step_execution = StepExecution.objects.create(
            workflow_execution=execution,
            step=first_step,
            status="pending"
        )

        step_execution.start()
    
        handler_map = {
            "email": email_workflow_execuction(
                to = step_execution.step.config["to"][0]
            ),
            "approval": approval_workflow_execuction,
            "task": task_workflow_execuction,
            "webhook": webhook_workflow_execuction,
        }

        handler = handler_map.get(first_step.step_type)
        if handler:
            handler(step_execution)

        return Response(
            WorkflowExecutionSerializer(execution).data,
            status=status.HTTP_201_CREATED
        )
<!-- urls -->
from django.urls import path
from . import views

urlpatterns = [
    path("execute-workflow/" , views.WorkflowExecutionView.as_view())
]

3 - customers app 
<!-- urls  -->
from restframework-simple_jwt.views import TokenObtainPerView , TokenRefreshView


urlpatterns = [
    path("token/" , TokenObtainPerView.as_view()),
    path("refresh/" , TokenRefreshView.as_view()),
]

<!-- users model -->

class User(AbstractUser) :
    ROLES_CHOICES = (
        ('owner','Owner'),
        ('admin','Admin'),
        ('manager','Manager'),
        ('employee','Employee')
    )

    role = models.CharField(max_length=100, choices=ROLES_CHOICES)

    def __str__(self):
        return self.role

<!-- executions model -->
from django.db import models
from typing import Dict, Any , Optional

class WorkflowExecution(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    workflow = models.ForeignKey(
        "workflows.Workflow",
        on_delete=models.CASCADE
    )
    triggered_by = models.ForeignKey(
        "customers.User",
        null=True,
        on_delete=models.SET_NULL
    )
    status   = models.CharField(max_length=20, choices=STATUS_CHOICES)
    context   = models.JSONField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta :
        ordering = ['-started_at']
    
    def initialize_context(self, inputs:Dict[str, Any] , metadata: Optional[Dict[str, Any]] = None):
        self.context = {
            "schema_version" : "1.0" , 
            "inputs":inputs , 
            "vacriables" : {} , 
            "metadata" : {
                "workflow_version" : getattr(self.workflow , 'version' , '1.0')
            },
            "state" : {
                "current_step":None , 
                "completed_step":[] , 
                "failed_step":[] ,
                "skipped_step":[] , 
            }
        }
        self.save()

class StepExecution(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("waiting", "Waiting"),
        ("done", "Done"),
        ("error", "Error"),
    )

    workflow_execution = models.ForeignKey(
        WorkflowExecution,
        related_name="steps",
        on_delete=models.CASCADE
    )
    step = models.ForeignKey(
        "workflows.WorkflowStep",
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    output = models.JSONField(null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def start(self):
        """
            Mark the step as running. ::
        """
        self.status = "running"
        self.save(update_fields=['status'])

<!-- workflow model  -->
from django.db import models
from customers.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class WorkFlow(models.Model) :
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey(User , on_delete=models.CASCADE , related_name='workflows')
    
    def __str__(self) :
        return self.name

class WorkFlowStep(models.Model) :

    STEPS_TYPE = (
        ('task','Task'),
        ('approval','Approval'),
        ('email','Email'),
        ('delay','Delay'),
        ('webhook','Webhook'),
    )

    workflow  = models.ForeignKey(WorkFlow , on_delete=models.CASCADE , related_name='steps')
    step_type = models.CharField(max_length=100 , choices=STEPS_TYPE)
    config    = models.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.workflow} {self.step_type}"

