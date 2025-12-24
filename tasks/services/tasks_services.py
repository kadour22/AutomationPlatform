from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from tasks.models import Task
from tasks.serializers import TaskSerializer


def tasks_list_service(request) :
    tasks = Task.objects.select_related("author").all().order_by("-created_at")
    serializer = TaskSerializer(
        tasks , many = True
    )
    return Response(serializer.data , status=200)

def delete_task_service(request,task_id) :
    task = get_object_or_404(Task , id = task_id)
    task.delete()
    return Response({
        "message" : f"task : {task.title} deleted "
    },status=200)