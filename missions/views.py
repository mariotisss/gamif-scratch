from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Mission
from .serializers import MissionSerializer

# Create your views here.
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAdminOrReadOnly]