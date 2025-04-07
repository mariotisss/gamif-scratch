from django.db import models

# Create your models here.
class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title