from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserTeam(models.Model):
    ROLE_CHOICES = [
        ("member", "Member"),
        ("admin", "Admin"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    class Meta:
        unique_together = ("user", "team")

    def __str__(self):
        return f"{self.user} - {self.team} ({self.role})"

class CopilotEngagementMetric(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    total_active_users = models.PositiveIntegerField()
    total_engaged_users = models.PositiveIntegerField()
    engagement_rate = models.FloatField(help_text="Ratio of engaged to active users (0.0 to 1.0)")

    class Meta:
        unique_together = ("team", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"Copilot metrics for {self.team.name} on {self.date} (Engagement: {self.engagement_rate:.2%})"
