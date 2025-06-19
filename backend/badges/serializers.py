from rest_framework import serializers
from .models import Badge, UserBadge, Reward

class BadgeSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Badge
        fields = '__all__'


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'awarded_at']


class RewardSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = Reward
        fields = ['id', 'mission', 'badge', 'xp_points']