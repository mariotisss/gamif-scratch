from rest_framework import serializers
from .models import Mission, UserMission
from django.contrib.auth import get_user_model
from gamification_project.utils.levels import user_level_from_xp
from analytics.models import Notification
from badges.utils import evaluate_dynamic_badges
from analytics.slack import send_slack_notification


User = get_user_model()

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission 
        fields = '__all__' 

class CompleteMissionSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user
        mission_id = data['mission_id']

        try:
            mission = Mission.objects.get(id=mission_id)
        except Mission.DoesNotExist:
            raise serializers.ValidationError("Mission does not exist.")

        if UserMission.objects.filter(user=user, mission=mission).exists():
            raise serializers.ValidationError("You have already completed this mission.")

        data['mission'] = mission
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        mission = validated_data['mission']
        return UserMission.objects.create(user=user, mission=mission)
