from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # No se muestra en respuestas

    class Meta:
        model = User
        fields = ('username', 'email', 'password') # Campos requeridos para registro

    def create(self, validated_data):
        # Se usa create_user para que Django hashee la contraseña
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
