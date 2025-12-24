from rest_framework.response import Response
from rest_framework import status

from tasks.models import Task
from tasks.serializers import TaskSerializer


def tasks_list_service(request) :
    tasks = Task.objects.select_related("author").all().order_by("-created_at")
    serializer = TaskSerializer(
        tasks , many = True
    )
    return Response(serializer.data , status=200)

