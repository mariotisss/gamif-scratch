from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Team, UserTeam
from .serializers import TeamSerializer, UserTeamSerializer

# Permite crear, listar, editar y eliminar equipos
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # No autenticados solo pueden leer

# Listar las relaciones UserTeam del usuario autenticado
class UserTeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTeamSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return UserTeam.objects.filter(user=self.request.user)
