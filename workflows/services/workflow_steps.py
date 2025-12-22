from rest_framework.response import Response
from rest_framework import status
from workflows.models import WorkFlowStep
from workflows.serializers import workflow_steps_serializer

def create_workflow_steps(data) :
    
    serializer = workflow_steps_serializer(data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=200)
    return Response(serializer.errors , status=404)


