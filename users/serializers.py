from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password]) # No se muestra en respuestas
    # He tenido que agregar el validador de contraseña para que no falle el test de registro

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
