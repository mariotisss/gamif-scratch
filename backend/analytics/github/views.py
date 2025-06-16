import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from missions.models import Mission, UserMission

@csrf_exempt
def github_webhook_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    event_type = request.headers.get("X-GitHub-Event")
    if event_type == "push":
        pusher_name = payload.get("pusher", {}).get("name")
        commits = payload.get("commits", [])
        if not pusher_name or not commits:
            return JsonResponse({"message": "No relevant data in push"}, status=200)

        try:
            user = CustomUser.objects.get(username=pusher_name)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": f"No user found for pusher: {pusher_name}"}, status=200)

        missions = Mission.objects.filter(type="github_commit")
        for mission in missions:
            if not UserMission.objects.filter(user=user, mission=mission).exists():
                UserMission.objects.create(user=user, mission=mission)

        return JsonResponse({"message": "Processed push event"}, status=200)

    return JsonResponse({"message": "Event type not handled"}, status=200)
