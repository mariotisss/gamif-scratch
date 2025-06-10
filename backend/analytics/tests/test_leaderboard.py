import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from badges.models import Badge, UserBadge
from teams.models import Team, UserTeam

User = get_user_model()

@pytest.mark.django_db
def test_leaderboard():
    user1 = User.objects.create_user(username="alice", password="pass123", xp=300, level=2)
    user2 = User.objects.create_user(username="bob", password="pass456", xp=500, level=3)

    badge1 = Badge.objects.create(
        name="Starter",
        description="Test badge",
        condition_code="test",
        icon=""
    )

    # Asignamos el mismo badge dos veces para simular múltiples premios
    UserBadge.objects.create(user=user1, badge=badge1)
    UserBadge.objects.create(user=user2, badge=badge1)  # intencionalmente duplicado

    client = APIClient()
    response = client.get("/api/leaderboard/")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) >= 2

    first = response.data[0]
    assert "username" in first
    assert "xp" in first
    assert "level" in first
    assert "badges" in first
    assert isinstance(first["badges"], int)


@pytest.mark.django_db
def test_leaderboard_filter_by_team():
    # Crear equipo
    team = Team.objects.create(name="Team A", description="Test Team")

    # Crear usuarios
    user1 = User.objects.create_user(username="alice", password="pass123", xp=500, level=3)
    user2 = User.objects.create_user(username="bob", password="pass456", xp=300, level=2)
    user3 = User.objects.create_user(username="charlie", password="pass789", xp=800, level=5)

    # Asignar solo dos usuarios al equipo
    UserTeam.objects.create(user=user1, team=team)
    UserTeam.objects.create(user=user2, team=team)

    client = APIClient()
    response = client.get(f"/api/leaderboard/?team={team.id}")

    assert response.status_code == status.HTTP_200_OK
    usernames = [entry["username"] for entry in response.data]

    assert "alice" in usernames
    assert "bob" in usernames
    assert "charlie" not in usernames


@pytest.mark.django_db
def test_leaderboard_limit_parameter():
    # Creo 5 usuarios con distintos valores de XP (de 100 a 500)
    for i in range(5):
        User.objects.create_user(
            username=f"user{i}",
            password="testpass",
            level=i + 1,
            xp=100 * ((i+1) ** 1.5) # XP creciente
        )

    client = APIClient()
    response = client.get("/api/leaderboard/?limit=3")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 3

    # Verifica que están en orden descendente por XP
    xps = [entry["xp"] for entry in response.data]
    assert xps == sorted(xps, reverse=True)
