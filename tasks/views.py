from tasks.services.tasks_services import (
    tasks_list_service , delete_task_service , create_task_service
)
from rest_framework.views import APIView

class tasks_view_logic(APIView) :
    
    def get(self, request) :
        return tasks_list_service(request=request)
    
    def post(self,request) :
        return create_task_service(user=request.user , data=request.data)
    
    def delete(self,request,task_id) :
        return delete_task_service(task_id=task_id)