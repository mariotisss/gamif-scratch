from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from teams.models import UserTeam
from rest_framework import status
from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer

User = get_user_model()

class LeaderboardView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        team_id = request.query_params.get("team")

        users = User.objects.all()

        if team_id:
            users = users.filter(userteam__team_id=team_id)

        users = users.order_by("-xp")[:limit]
        data = [
            {
                "id": u.id,
                "username": u.username,
                "xp": u.xp,
                "level": u.level,
                "badges": u.user_badges.count()
            }
            for u in users
        ]
        return Response(data, status=status.HTTP_200_OK)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')