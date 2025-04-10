from rest_framework import serializers
from .models import Mission, UserMission
from django.contrib.auth import get_user_model

User = get_user_model()

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission 
        fields = '__all__' 

class CompleteMissionSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField() # Se espera solo el ID de la misión

    def validate_mission_id(self, value):
         # Validar que existe
        try:
            Mission.objects.get(id=value)
        except Mission.DoesNotExist:
            raise serializers.ValidationError("La misión no existe.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user     # Usuario autenticado
        mission = Mission.objects.get(id=validated_data['mission_id'])

        if UserMission.objects.filter(user=user, mission=mission).exists():
            raise serializers.ValidationError("Ya has completado esta mision.")

        # Registrar misión como completada y otorgar XP
        UserMission.objects.create(user=user, mission=mission)
        user.xp += mission.xp_reward
        user.save()

        return {
            "message": "Mision completada",
            "new_xp": user.xp
        }
