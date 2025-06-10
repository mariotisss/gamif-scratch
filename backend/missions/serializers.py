from rest_framework import serializers
from .models import Mission, UserMission
from django.contrib.auth import get_user_model
from gamification_project.utils.levels import user_level_from_xp
from analytics.models import Notification
from badges.utils import evaluate_dynamic_badges


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
        user = self.context['request'].user
        mission = Mission.objects.get(id=validated_data['mission_id'])

        if UserMission.objects.filter(user=user, mission=mission).exists():
            raise serializers.ValidationError("Ya has completado esta mision.")

        # Registrar misión como completada, otorgar XP y actualizar nivel
        # En caso de subir nivel, crear notificación
        UserMission.objects.create(user=user, mission=mission)
        user.xp += mission.xp_reward

        old_level = user.level  # Se almacena nivel previo
        new_level = user_level_from_xp(user.xp)  # Nuevo cálculo de nivel
        user.level = new_level
        user.save()

        # Evaluar medallas dinamicamente
        evaluate_dynamic_badges(user)

        # Si subió de nivel, creamos notificación
        if new_level > old_level:
            Notification.objects.create(
                user=user,
                type='leveled_up',
                message=f"Awesome! You leveled up to level {new_level}.",
                related_object_id=None
            )

        return {
            "message": "Mision completada",
            "new_xp": user.xp,
            "new_level": user.level
        }
