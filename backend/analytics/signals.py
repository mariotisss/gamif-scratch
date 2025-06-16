from django.db.models.signals import post_save
from django.dispatch import receiver
from missions.models import UserMission
from badges.models import UserBadge
from gamification_project.utils.levels import user_level_from_xp
from .models import Notification
from badges.utils import evaluate_dynamic_badges
from analytics.slack import send_slack_notification


@receiver(post_save, sender=UserMission)
def on_mission_completed(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        mission = instance.mission

        # Añadir XP y calcular nivel
        user.xp += mission.xp_reward
        old_level = user.level
        new_level = user_level_from_xp(user.xp)
        user.level = new_level
        user.save()

        # Evaluar medallas dinámicas
        evaluate_dynamic_badges(user)

        # Notificación de misión completada
        Notification.objects.create(
            user=user,
            type='mission_completed',
            message=f"Congratulations! You completed the mission '{mission.title}'.",
            related_object_id=mission.id
        )
        send_slack_notification(f":checkered_flag: *{user.username}* completed mission: *{mission.title}*")

        # Si sube de nivel
        if new_level > old_level:
            Notification.objects.create(
                user=user,
                type='leveled_up',
                message=f"Awesome! You leveled up to level {new_level}.",
                related_object_id=None
            )
            send_slack_notification(f":arrow_up: *{user.username}* leveled up to *Level {new_level}*!")


@receiver(post_save, sender=UserBadge)
def on_badge_earned(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            type='badge_earned',
            message=f"You have earned a new badge: '{instance.badge.name}'.",
            related_object_id=instance.badge.id
        )
        send_slack_notification(f":trophy: *{instance.user.username}* earned a new badge: *{instance.badge.name}*")