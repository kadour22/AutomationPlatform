from rest_framework.response import Response
from rest_framework.views import APIView
from approvals.services.services import (
    create_approval, get_approvals,
    delete_approval, single_approval
)
from .permissions import IsEmployeePermission

class approvals_list(APIView) :
    permission_classes = [IsEmployeePermission]
    def get(self, request) :
        return get_approvals(request=request)

class approval_detail(APIView) :
    permission_classes = [IsEmployeePermission]
    def get(self, request, approval_id) :
        return single_approval(approval_id=approval_id)

class approval_delete(APIView) :
    permission_classes = [IsEmployeePermission]
    def delete(self, request, approval_id) :
        return delete_approval(approval_id=approval_id)

class create_approval_view(APIView) :
    permission_classes = [IsEmployeePermission]
    def post(self, request) :
        return create_approval(data=request.data , requester=request.user)