from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'type', 'message', 'created_at', 'read', 'related_object_id']
        read_only_fields = ['id', 'created_at']
