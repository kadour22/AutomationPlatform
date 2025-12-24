from workflows.models import WorkFlow
from workflows.serializers import workflow_serializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

def workflow_list(request) :
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