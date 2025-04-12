import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from missions.models import Mission

User = get_user_model()

@pytest.mark.django_db
def test_complete_mission_gain_xp():
    # Crear usuario y misión
    user = User.objects.create_user(username="completer", password="test1234", xp=0)
    mission = Mission.objects.create(title="Test Mission", description="XP gain", xp_reward=100)

    # Obtener token JWT
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "completer", "password": "test1234"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Completar mision
    response = client.post(reverse("complete_mission"), {
        "mission_id": mission.id
    }, format="json")

    user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert "Mision completada" in response.data["message"]
    assert user.xp == 100