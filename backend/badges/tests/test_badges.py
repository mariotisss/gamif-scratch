import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from badges.models import Badge

User = get_user_model()

@pytest.mark.django_db
def test_create_badge_as_admin():
    admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "admin",
        "password": "adminpass"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("badges-list"), {
        "name": "Starter Badge",
        "description": "First achievement",
        # "icon": "",  El test detecta esto como una cadena vacia y da error, por eso lo dejo comentado
        "condition_code": "starter_code"
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Badge.objects.filter(name="Starter Badge").exists()

@pytest.mark.django_db
def test_assign_badge_to_user():
    user = User.objects.create_user(username="badgeuser", password="userpass")
    badge = Badge.objects.create(name="Test Badge", description="For testing", icon="", condition_code="test_code")

    client = APIClient()
    token = client.post(reverse("token_obtain_pair"), {
        "username": "badgeuser",
        "password": "userpass"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("assign_badge"), {
        "badge_id": badge.id
    }, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert user.user_badges.filter(badge=badge).exists()
