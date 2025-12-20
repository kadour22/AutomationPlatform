from .models import WorkFlowStep , WorkFlow
from rest_framework import serializers


class workflow_serializer(serializers.ModelSerializer) :
    class Meta :
        model = WorkFlow
        fields = "__all__"
        read_only_fields = ['created_by']