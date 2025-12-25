from approvals.models import Approval
from approvals.serializers import ApprovalSerializer

from rest_framework.response import Response
def create_approval(data , requester):
    serializer = ApprovalSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(requester=requester)
        return Response(serializer.data,status=201)