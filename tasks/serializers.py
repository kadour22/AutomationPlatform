from rest_framework import serializers
from .models import Task
from django.core.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Task
        fields = [
            "title" , "content" , "author" , "created_at"
        ]
        read_only_fields = ["author"]

    def validate(self , attrs) :
        if attrs["title"] == "" or attrs["content"] == "" :
            raise ValidationError("title and content is required")
        
        return attrs