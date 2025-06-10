import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from missions.models import Mission

User = get_user_model()

@pytest.mark.django_db
def test_create_mission_unauthenticated():
    client = APIClient()
    response = client.post(reverse("missions-list"), {
        "title": "Unauth Mission",
        "description": "Should fail",
        "xp_reward": 10
    }, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_create_mission_as_normal_user_forbidden():
    user = User.objects.create_user(username="basic", password="12345")
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "basic", "password": "12345"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("missions-list"), {
        "title": "Forbidden Mission",
        "description": "Not admin",
        "xp_reward": 20
    }, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_complete_nonexistent_mission():
    user = User.objects.create_user(username="completer", password="12345")
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "completer", "password": "12345"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("complete_mission"), {
        "mission_id": 9999
    }, format="json")
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]
