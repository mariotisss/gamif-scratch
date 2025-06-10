import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

# Creacion de usuario de prueba
@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post(reverse('register'), {
        "username": "testuser",
        "password": "securepassword123",
        "email": "test@example.com"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser").exists()

# Prueba de inicio de sesion
@pytest.mark.django_db
def test_user_login_and_token():
    user = User.objects.create_user(username="tester", password="pass1234")
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {
        "username": "tester",
        "password": "pass1234"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

# Prueba mostrar usuario autenticado
@pytest.mark.django_db
def test_user_me_authenticated():
    user = User.objects.create_user(username="meuser", password="me123456")
    client = APIClient()
    token = client.post(reverse('token_obtain_pair'), {
        "username": "meuser", "password": "me123456"
    }).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get(reverse('user_me'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "meuser"

# Prueba mostrar usuario no autenticado (error)
@pytest.mark.django_db
def test_user_me_unauthenticated():
    client = APIClient()
    response = client.get(reverse('user_me'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
