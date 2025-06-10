import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from analytics.models import Notification

User = get_user_model()

@pytest.mark.django_db
def test_create_notification_as_admin():
    admin = User.objects.create_superuser(username="admin", password="admin123")
    user = User.objects.create_user(username="johnny", password="test123")

    client = APIClient()
    client.force_authenticate(user=admin)

    payload = {
        "user": user.id,
        "type": "badge_earned",
        "message": "This is a test notification."
    }

    response = client.post("/api/notifications/", payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Notification.objects.count() == 1

@pytest.mark.django_db
def test_list_my_notifications():
    user = User.objects.create_user(username="jane", password="test123")
    Notification.objects.create(user=user, type="info", message="First")

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/notifications/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["message"] == "First"

@pytest.mark.django_db
def test_cant_list_others_notif():
    user1 = User.objects.create_user(username="user1", password="test123")
    user2 = User.objects.create_user(username="user2", password="test123")

    Notification.objects.create(user=user2, type="info", message="Hidden")

    client = APIClient()
    client.force_authenticate(user=user1)

    response = client.get("/api/notifications/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

@pytest.mark.django_db
def test_mark_notification_as_read():
    user = User.objects.create_user(username="lucy", password="test123")
    notif = Notification.objects.create(user=user, type="info", message="Unread")

    client = APIClient()
    client.force_authenticate(user=user)

    url = f"/api/notifications/{notif.id}/"
    response = client.patch(url, {"read": True}, format='json')
    assert response.status_code == status.HTTP_200_OK

    notif.refresh_from_db()
    assert notif.read is True

@pytest.mark.django_db
def test_unauthenticated_access_denied():
    client = APIClient()
    response = client.get("/api/notifications/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
