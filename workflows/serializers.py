from .models import WorkFlowStep , WorkFlow
from rest_framework import serializers
from workflows.validtors.step_validator import validate_step_config

class workflow_serializer(serializers.ModelSerializer) :
    class Meta :
        model = WorkFlow
        fields = ["name","description","created_by","created_at"]
        read_only_fields = ['created_by']


class workflow_steps_serializer(serializers.ModelSerializer) :
    class Meta :
        model = WorkFlowStep
        fields = "__all__"
    
    def validate(self , data) :
        step_type = data.get('step_type')
        config = data.get('config')

        validate_step_config(step_type , config)

        return data
    
    