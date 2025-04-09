from django.db import models
from django.conf import settings

class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UserMission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mission')  # evitar duplicados

    def __str__(self):
        return f"{self.user.username} -> {self.mission.title}"