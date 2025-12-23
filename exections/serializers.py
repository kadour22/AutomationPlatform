from rest_framework import serializers
from exections.models import WorkflowExecution , StepExecution


class WorkflowExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowExecution
        fields = '__all__'