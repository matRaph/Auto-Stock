from django.contrib.auth.models import Group, User
from rest_framework import serializers

from app.models import CarModel, Part


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[("admin", "Administrador"), ("normal", "Comum")],
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)

        if role == "admin":
            group = Group.objects.get(name="Administrador")
        else:
            group = Group.objects.get(name="Comum")

        user.groups.add(group)
        return user
