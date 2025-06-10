from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import Badge, UserBadge, Reward
from .serializers import BadgeSerializer, UserBadgeSerializer, RewardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AssignBadgeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        badge_id = request.data.get("badge_id")
        try:
            badge = Badge.objects.get(pk=badge_id)
        except Badge.DoesNotExist:
            return Response({"error": "Badge not found"}, status=status.HTTP_404_NOT_FOUND)

        UserBadge.objects.create(user=request.user, badge=badge)
        return Response({"message": "Badge assigned"}, status=status.HTTP_200_OK)