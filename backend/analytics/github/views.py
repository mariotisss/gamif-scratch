import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from users.models import CustomUser
from missions.models import Mission
from analytics.github.models import GithubEvent
from analytics.github.utils import eval_github_event

@csrf_exempt
def github_webhook_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    event_type = request.headers.get("X-GitHub-Event")
    pusher_name = payload.get("pusher", {}).get("name")

    try:
        user = CustomUser.objects.get(username=pusher_name)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": f"No user found for pusher: {pusher_name}"}, status=200)

    if event_type == "push":
        commits = payload.get("commits", [])
        for commit in commits:
            commit_id = commit.get("id")
            timestamp = parse_datetime(commit.get("timestamp"))

            if not GithubEvent.objects.filter(github_id=commit_id).exists():
                GithubEvent.objects.create(
                    user=user,
                    event_type="commit",
                    github_id=commit_id,
                    timestamp=timestamp
                )

    elif event_type == "pull_request":
        pr = payload.get("pull_request", {})
        pr_id = str(pr.get("id"))
        timestamp = parse_datetime(pr.get("created_at"))

        if pr_id and timestamp and not GithubEvent.objects.filter(github_id=pr_id).exists():
            GithubEvent.objects.create(
                user=user,
                event_type="pull_request",
                github_id=pr_id,
                timestamp=timestamp
            )

    # Evaluar misiones dinámicas de tipo github_event
    github_missions = Mission.objects.filter(type="github_event", is_active=True)
    for mission in github_missions:
        eval_github_event(user, mission)

    return JsonResponse({"message": "GitHub event processed"}, status=200)

