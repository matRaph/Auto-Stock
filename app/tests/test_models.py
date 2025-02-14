import pytest

from app.models import CarModel, Part


@pytest.mark.django_db
def test_create_part():
    part = Part.objects.create(
        part_number="XPTO1234", name="Filtro de Óleo", details="Filtro de alta qualidade", price=45.00, quantity=50
    )
    assert part.part_number == "XPTO1234"
    assert part.name == "Filtro de Óleo"
    assert part.price == 45.00
    assert part.quantity == 50


@pytest.mark.django_db
def test_create_car_model():
    car_model = CarModel.objects.create(name="Model S", manufacturer="Tesla", year=2022)
    assert car_model.name == "Model S"
    assert car_model.manufacturer == "Tesla"
    assert car_model.year == 2022
