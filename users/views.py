from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Cualquier usuario puede registrarse
    serializer_class = RegisterSerializer

class UserMeView(APIView):
    permission_classes = [IsAuthenticated] # Login con token JWT

    def get(self, request):
        user = request.user
        return Response({ # Info del usuario logueado
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "xp": user.xp,
            "level": user.level
        })