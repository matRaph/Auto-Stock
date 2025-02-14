import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import CarModel, Part


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = User.objects.create_user(username="admin", password="admin123")
    user.groups.set([1])
    return user


@pytest.fixture
def part():
    return Part.objects.create(
        part_number="XPTO1234", name="Filtro de Óleo", details="Filtro de alta qualidade", price=45.00, quantity=50
    )


@pytest.fixture
def car_model():
    return CarModel.objects.create(name="Model S", manufacturer="Tesla", year=2022)


@pytest.mark.django_db
def test_list_parts(api_client, admin_user, part):
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_retrieve_part(api_client, admin_user, part):
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-detail", args=[part.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["part_number"] == "XPTO1234"


@pytest.mark.django_db
def test_list_car_models(api_client, admin_user, car_model):
    api_client.force_authenticate(user=admin_user)
    url = reverse("car_model-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_retrieve_car_model(api_client, admin_user, car_model):
    api_client.force_authenticate(user=admin_user)
    url = reverse("car_model-detail", args=[car_model.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Model S"
