from django.db import models
from users.models import CustomUser

class GithubEvent(models.Model):
    EVENT_TYPES = [
        ("commit", "Commit"),
        ("pull_request", "Pull Request"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    github_id = models.CharField(max_length=64, unique=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"
