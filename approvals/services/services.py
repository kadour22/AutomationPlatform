from approvals.models import Approval
from approvals.serializers import ApprovalSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

def create_approval(data , requester):
    serializer = ApprovalSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(requester=requester)
        return Response(serializer.data,status=201)
    return Response(serializer.errors, status=400)

def get_approvals(request):
    approvals = Approval.objects.all()
    serializer = ApprovalSerializer(approvals, many=True)
    return Response(serializer.data, status=200)

def delete_approval(approval_id):
    try:
        approval = Approval.objects.get(id=approval_id)
        approval.delete()
        return Response(status=204)
    except Approval.DoesNotExist:
        return Response({"error": "Approval not found."}, status=404)

def single_approval(approval_id) :
    approval = get_object_or_404(Approval, id=approval_id)
    serializer = ApprovalSerializer(approval)
    return Response(serializer.data, status=200)
