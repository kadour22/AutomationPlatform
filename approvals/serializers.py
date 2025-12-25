from rest_framework import serializers
from .models import Approval

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['id', 'requester', 'content', 'approved', 'timestamp']