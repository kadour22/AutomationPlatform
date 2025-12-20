from workflows.models import WorkFlow
from workflows.serializers import workflow_serializer
from rest_framework.response import Response
from rest_framework import status


def workflow_list() :
    workflows  = WorkFlow.objects.select_related("created_by").all()
    serializer = workflow_serializer(
        workflows , many=True
    ) 
    return Response(serializer.data , status=200)