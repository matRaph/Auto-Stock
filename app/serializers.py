from django.contrib.auth.models import Group, User
from rest_framework import serializers

from app.models import CarModel, Part


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        exclude = ["car_model"]


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class CarModelDetailSerializer(serializers.ModelSerializer):
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = ["id", "name", "manufacturer", "year", "parts"]


class PartDetailSerializer(serializers.ModelSerializer):
    car_models = CarModelSerializer(many=True, read_only=True)

    class Meta:
        model = Part
        fields = ["id", "part_number", "name", "details", "price", "quantity", "updated_at", "car_models"]


class VinculoParteSerializer(serializers.Serializer):
    part_id = serializers.IntegerField()

    def validate_part_id(self, value):
        if not Part.objects.filter(id=value).exists():
            raise serializers.ValidationError("Parte não encontrada.")
        return value

    def vincular_parte(self, car_model):
        part = Part.objects.get(id=self.validated_data["part_id"])
        car_model.parts.add(part)

    def desvincular_parte(self, car_model):
        part = Part.objects.get(id=self.validated_data["part_id"])
        car_model.parts.remove(part)


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


class ImportPartSerializer(serializers.Serializer):
    file = serializers.FileField()
