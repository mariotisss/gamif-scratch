from django.db import models
from django.conf import settings
from datetime import timedelta

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
            ("github_event", "GitHub Event"),
            # Exensiones futuras a otras plataformas
        ],
        default="manual"
    )

    metadata = models.JSONField(blank=True, null=True) # Informacion adicional, como condiciones o tipo
    '''
        {
            "event_type": "commit",
            "threshold": 3,
            "period": "daily"
        }
    '''
    # Limite de tiempo para completar la misión (en días)
    time_limit_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Días desde la creación para completar la misión. Dejar vacío si no hay límite."
    )

    # Calcula la fecha de expiración de la misión
    def expiration_date(self):
        if self.time_limit_days is not None:
            return self.created_at + timedelta(days=self.time_limit_days)
        return None

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