from rest_framework import serializers 
from .models import User
from django.core.exceptions import ValidationError


class customer_serializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields= "__all__"
    
    def validate(self,attrs) :
        if attrs["role"] == "" :
            raise ValidationError(
                "Role field is required"
            )
        return attrs
    
    def create(self, validated_data):
       password = validated_data.pop('password')
       user = User.objects.create_user(**validated_data, password=password)
       return user
