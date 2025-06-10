from django.db.models.signals import post_save
from django.dispatch import receiver
from missions.models import UserMission
from badges.models import UserBadge
from .models import Notification

@receiver(post_save, sender=UserMission)
def on_mission_completed(sender, instance, created, **kwargs):
    if created and instance.completed_at:
        Notification.objects.create(
            user=instance.user,
            type='mission_completed',
            message=f"Congratulations! You completed the mission '{instance.mission.title}'.",
            related_object_id=instance.mission.id
        )
        # Aquí se podria llamar a la funcion para enviar notificacion a Slack

@receiver(post_save, sender=UserBadge)
def on_badge_earned(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            type='badge_earned',
            message=f"You have earned a new badge: '{instance.badge.name}'.",
            related_object_id=instance.badge.id
        )
        # Aquí se podria llamar a la funcion para enviar notificacion a Slack
