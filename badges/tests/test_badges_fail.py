import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_assign_nonexistent_badge():
    user = User.objects.create_user(username="testuser", password="pass1234")
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "testuser",
        "password": "pass1234"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("assign_badge"), {
        "badge_id": 9999  # ID inexistente
    }, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Badge not found"

@pytest.mark.django_db
def test_create_badge_missing_field():
    admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "admin",
        "password": "adminpass"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Falta condition_code
    response = client.post(reverse("badges-list"), {
        "name": "Incomplete Badge",
        "description": "Missing condition_code"
    }, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "condition_code" in response.data
