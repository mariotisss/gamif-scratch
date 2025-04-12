import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

# Creacion de mision exitosa (usuario admin)
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

# Creacion de mision fallida (usuario normal)
@pytest.mark.django_db
def test_create_mission_as_normal_user():
    user = User.objects.create_user(username="normal", password="userpass")
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "normal", "password": "userpass"
    }).data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("missions-list"), {
        "title": "User Mission",
        "description": "Should not be allowed",
        "xp_reward": 20
    }, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN