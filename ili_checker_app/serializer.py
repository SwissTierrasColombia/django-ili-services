from rest_framework import serializers
from ili_checker_app.models import *


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']  # Asegúrate de incluir 'password' aquí

    def create(self, validated_data):
        # Extraer y encriptar la contraseña antes de crear el usuario
        password = validated_data.pop('password', None)
        usuario = User(**validated_data)
        if password is not None:
            usuario.set_password(password)
        usuario.save()
        return usuario


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = "__all__"


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = "__all__"


class ReglaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regla
        fields = "__all__"
