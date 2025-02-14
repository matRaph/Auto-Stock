import pytest

from app.models import CarModel, Part
from app.serializers import CarModelSerializer, PartSerializer, VinculoParteSerializer


@pytest.mark.django_db
def test_part_serializer():
    part = Part.objects.create(
        part_number="XPTO1234", name="Filtro de Óleo", details="Filtro de alta qualidade", price=45.00, quantity=50
    )
    serializer = PartSerializer(part)
    assert serializer.data["part_number"] == "XPTO1234"
    assert serializer.data["name"] == "Filtro de Óleo"


@pytest.mark.django_db
def test_car_model_serializer():
    car_model = CarModel.objects.create(name="Model S", manufacturer="Tesla", year=2022)
    serializer = CarModelSerializer(car_model)
    assert serializer.data["name"] == "Model S"
    assert serializer.data["manufacturer"] == "Tesla"


@pytest.mark.django_db
def test_vinculo_parte_serializer():
    part = Part.objects.create(
        part_number="XPTO1234", name="Filtro de Óleo", details="Filtro de alta qualidade", price=45.00, quantity=50
    )
    data = {"part_id": part.id}
    serializer = VinculoParteSerializer(data=data)
    assert serializer.is_valid()
