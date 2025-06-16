from django.db import models
from django.conf import settings

class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)   # Si la misión esta disponible o no
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=30,
        choices=[
            ("manual", "Manual"),
            ("github_commit", "GitHub Commit"),
            ("github_pr", "GitHub Pull Request"),
        ],
        default="manual"
    )

    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class UserMission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True) # Fecha de finalización de la misión

    class Meta:
        unique_together = ('user', 'mission')  # Evita repetir la misma misión para el mismo usuario

    def __str__(self):
        return f"{self.user.username} -> {self.mission.title}"