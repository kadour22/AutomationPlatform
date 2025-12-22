from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from workflows.models import WorkFlowStep
from workflows.serializers import workflow_steps_serializer
from workflows.services.workflow_services import (
    workflow_list , get_workflow_by_id , delete_workflow
)

from workflows.services.workflow_steps import create_workflow_steps

class workflow_api_list(APIView) :
    def get(self, request) :
        return workflow_list()

class workflow_by_ID(APIView) :
    def get(self, request, workflow_id) :
        return get_workflow_by_id(workflow_id=workflow_id)
    
class delete_workflow_view(APIView) :
    def delete(self, request , workflow_id) :
        return delete_workflow(workflow_id=workflow_id)
    
class create_workflow_steps_view(APIView) :
    def post(self, request) :
        return create_workflow_steps(data=request.data)