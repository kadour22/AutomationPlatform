from tasks.services.tasks_services import (
    tasks_list_service , delete_task_service
)

from rest_framework.views import APIView



class tasks_view_logic(APIView) :
    def get(self, request,task_id=None) :
        return 