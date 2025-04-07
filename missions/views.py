from rest_framework import viewsets, permissions
from .models import Mission
from .serializers import MissionSerializer

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
    permission_classes = [IsAdminOrReadOnly]