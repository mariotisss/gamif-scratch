from rest_framework import serializers
from .models import Team, UserTeam
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'member_count']



class UserTeamSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    joined_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserTeam
        fields = ['id', 'user', 'team', 'role', 'joined_at']