from .serializers import WorkflowExecutionSerializer , StepExecution
from .models import WorkflowExecution
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .services.workflows_executions import email_workflow_execuction , approval_workflow_execuction , webhook_workflow_execuction , task_workflow_execuction

class WorkflowExecutionView(CreateModelMixin, GenericAPIView):
    serializer_class = WorkflowExecutionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = serializer.validated_data["workflow"]
        triggered_by = serializer.validated_data.get("triggered_by")

        # 1. Create execution FIRST (context will be set after)
        execution = WorkflowExecution.objects.create(
            workflow=workflow,
            triggered_by=triggered_by,
            status="running",
            context={},  # temporary, will be initialized properly
        )

        # 2. Initialize context correctly
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

        # 3. Create first step execution
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

        # 4. Dispatch handler
        handler_map = {
            "email": email_workflow_execuction,
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
