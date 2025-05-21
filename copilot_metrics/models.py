from django.db import models
from teams.models import Team, UserTeam


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
