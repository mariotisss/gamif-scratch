import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from missions.models import Mission

User = get_user_model()

# Creacion de mision (usuario admin)
@pytest.mark.django_db
def test_create_mission_as_admin():
    admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "admin", "password": "adminpass"
    }).data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("missions-list"), {
        "title": "Admin Mission",
        "description": "Created by admin",
        "xp_reward": 50
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Admin Mission"

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

# Para prevenir doble finalizacion y verificar cambios de nivel 
# ya hare otro test mas adelante! Dejo esto para acordarme