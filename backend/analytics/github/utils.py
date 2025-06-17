from django.utils.timezone import now, timedelta
from analytics.github.models import GithubEvent
from missions.models import UserMission

def eval_github_event(user, mission):
    """
    Checks if the user has met the criteria to complete a GitHub-based mission,
    based on metadata stored in the mission object.
    """
    condition = mission.metadata or {} # Default to empty dict if metadata is None
    event_type = condition.get("event_type", "commit")  # Default to "commit" if not specified
    threshold = condition.get("threshold", 1) # Default threshold to 1 if not specified
    period = condition.get("period", "daily") # Default to "daily" if not specified

    today = now()

    if period == "daily":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start_date = today - timedelta(days=today.weekday())
    elif period == "monthly":
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        return False

    count = GithubEvent.objects.filter(
        user=user,
        event_type=event_type,
        timestamp__gte=start_date
    ).count()

    if count >= threshold and not UserMission.objects.filter(user=user, mission=mission).exists():
        UserMission.objects.create(user=user, mission=mission)
        return True

    return False
