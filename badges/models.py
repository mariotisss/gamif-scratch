from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    condition_code = models.CharField(max_length=100, help_text="Codigo de condicion para desbloqueo (para logica interna)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        

# Relación entre usuario y badge
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} → {self.badge.name}"
    

# Relación entre badge y mision
class Reward(models.Model):
    mission = models.OneToOneField('missions.Mission', on_delete=models.CASCADE, related_name='reward', null=True, blank=True)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    xp_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reward: {self.xp_points} XP + Badge: {self.badge.name if self.badge else 'None'}"