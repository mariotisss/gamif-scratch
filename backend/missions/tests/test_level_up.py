import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from missions.models import Mission

User = get_user_model()

@pytest.mark.django_db
def test_user_levels_up_after_completing_mission():
    # Crear usuario con XP cercana al cambio de nivel
    user = User.objects.create_user(username="leveluser", password="test123", xp=90, level=1)
    mission = Mission.objects.create(title="Level Up Mission", description="Test level up", xp_reward=50)

    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "leveluser", "password": "test123"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("complete_mission"), {
        "mission_id": mission.id
    }, format="json")

    user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user.xp >= 140
    assert user.level > 1
