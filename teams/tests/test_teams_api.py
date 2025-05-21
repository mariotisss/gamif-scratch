import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from teams.models import Team, UserTeam

User = get_user_model()

@pytest.mark.django_db
def test_create_and_show_teams():
    user = User.objects.create_user(username="tester", password="pass123")
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "tester",
        "password": "pass123"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Crear equipo
    response_create = client.post("/api/teams/", {
        "name": "Equipo Test",
        "description": "Descripción del equipo"
    }, format="json")

    assert response_create.status_code == status.HTTP_201_CREATED
    assert Team.objects.filter(name="Equipo Test").exists()

    # Mostrar equipos
    response_list = client.get("/api/teams/")
    assert response_list.status_code == status.HTTP_200_OK
    assert any(team["name"] == "Equipo Test" for team in response_list.data)

@pytest.mark.django_db
def test_user_team_viewset_filters_by_user():
    user1 = User.objects.create_user(username="user1", password="abcd123")
    user2 = User.objects.create_user(username="user2", password="defg456")
    team1 = Team.objects.create(name="Team X", description="Equipo X")

    UserTeam.objects.create(user=user1, team=team1)
    UserTeam.objects.create(user=user2, team=team1)

    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "user1",
        "password": "abcd123"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get("/api/user-teams/")
    assert response.status_code == status.HTTP_200_OK
    assert all(entry["user"] == "user1" for entry in response.data)