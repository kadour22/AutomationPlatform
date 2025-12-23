from .serializers import WorkflowExecutionSerializer , StepExecution
from .models import WorkflowExecution
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .services.workflows_executions import email_workflow_execuction , approval_workflow_execuction , webhook_workflow_execuction , task_workflow_execuction

class WorkflowExecutionView(CreateModelMixin, GenericAPIView):
    serializer_class = WorkflowExecutionSerializer

    def post(self , request) :
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid() :
         
            # WorkflowExecution creation
            workflow     = serializer.validated_data['workflow']
            triggered_by = serializer.validated_data['triggered_by']
            execution = WorkflowExecution.objects.create(
                workflow , triggered_by
            )
            execution.initialize_context(
                inputs = {
                    "user_id" : triggered_by.id if triggered_by else None ,
                    "workflow_id" : workflow.id
                },
                
                metadata = {
                    "executed by" : triggered_by.username if triggered_by else "system" ,
                    "workflow name" : workflow.name
                }
            )
            execution.status = 'running'
            execution.save()

            # WorkflowStepExecutions 
            step = StepExecution.objects.create(
                workflow_execution=execution,
                step = execution.workflow.steps.first(),
                status='pending'
            )
            step.start()
            step.save()        
            handler_map = {
                        "email": email_workflow_execuction,
                        "approval": approval_workflow_execuction,
                        "task": task_workflow_execuction,
                        "webhook": webhook_workflow_execuction,
                    }
            handler = handler_map.get(step.step.step_type)
            if handler:
                handler(step)
            return Response(
            WorkflowExecutionSerializer(execution).data,
            status=status.HTTP_201_CREATED
        )