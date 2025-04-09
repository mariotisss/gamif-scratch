from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Mission
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
    permission_classes = [IsAdminOrReadOnly]

class CompleteMissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompleteMissionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
