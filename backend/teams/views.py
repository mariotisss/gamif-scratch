from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team, UserTeam
from .serializers import TeamSerializer, UserTeamSerializer
from missions.models import UserMission
from django.contrib.auth import get_user_model
User = get_user_model()


# Permite crear, listar, editar y eliminar equipos
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # No autenticados solo pueden leer

    # Aqui se añade automaticamente el endpoint /teams/<id>/members. No hay que definir en el router
    @action(detail=True, methods=["get"], url_path="members", permission_classes=[permissions.IsAuthenticated])
    def members(self, request, pk=None):
        team = self.get_object()
        members = UserTeam.objects.filter(team=team)
        serializer = UserTeamSerializer(members, many=True)
        return Response(serializer.data)
    
    # Endpoint para unirse a un equipo /teams/ranking
    @action(detail=False, methods=["get"], url_path="ranking", permission_classes=[permissions.IsAuthenticated])
    def ranking(self, request):
        teams = Team.objects.all()
        data = []

        for team in teams:
            members = User.objects.filter(userteam__team=team)
            total_misiones = UserMission.objects.filter(user__in=members).count()

            data.append({
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "missions_completed": total_misiones,
            })

        data.sort(key=lambda x: x["missions_completed"], reverse=True)
        return Response(data)


# Listar las relaciones UserTeam del usuario autenticado
class UserTeamViewSet(viewsets.ModelViewSet):
    queryset = UserTeam.objects.all()
    serializer_class = UserTeamSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return UserTeam.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
