from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncDate
from django.db.models import Count
from .models import Mission, UserMission
from .serializers import MissionSerializer, CompleteMissionSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS --> Permite lectura a cualquier usuario
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite escritura solo a usuarios administradores
        # (is_staff es un atributo de User que indica si el usuario es admin)
        return request.user and request.user.is_staff

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAdminOrReadOnly] # Admin: crear/editar; Resto: ver


class CompleteMissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompleteMissionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()  # Completa la misión y actualiza XP
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MissionStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        stats = (
            UserMission.objects
            .filter(user=user)
            .annotate(date=TruncDate('completed_at'))
            .values('date')
            .annotate(completed=Count('id'))
            .order_by('date')
        )
        return Response(stats, status=status.HTTP_200_OK)
