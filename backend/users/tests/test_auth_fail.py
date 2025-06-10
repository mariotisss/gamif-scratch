import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_register_weak_password():
    client = APIClient()
    response = client.post(reverse('register'), {
        "username": "weakuser",
        "password": "123",  # password demasiado corta
        "email": "weak@example.com"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_invalid_credentials():
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {
        "username": "invaliduser",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access" not in response.data

@pytest.mark.django_db
def test_access_me_without_token():
    client = APIClient()
    response = client.get(reverse('user_me'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
