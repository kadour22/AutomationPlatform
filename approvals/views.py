from rest_framework.response import Response
from rest_framework.views import APIView
from approvals.services.services import (
    create_approval, get_approvals,
    delete_approval, single_approval
)

class approvals_list(APIView) :
    def get(self, request) :
        return get_approvals(request=request)
