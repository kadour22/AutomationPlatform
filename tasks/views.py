from tasks.services.tasks_services import (
    tasks_list_service , delete_task_service , create_task_service
)
from rest_framework.views import APIView
from workflows.permmsions import IsOwnerPermission , ManagerPermission


class tasks_lists_view(APIView) :
    permission_classes = [IsOwnerPermission | ManagerPermission]

    def get(self, request) :
        return tasks_list_service(request=request)

class create_task_view(APIView) :
    permission_classes = [IsOwnerPermission | ManagerPermission]
    def post(self,request) :
        return create_task_service(data=request.data, author=request.user)

class delete_task_view(APIView) :
    permission_classes = [IsOwnerPermission | ManagerPermission]

    def delete(self,request,task_id) :
        return delete_task_service(task_id=task_id)