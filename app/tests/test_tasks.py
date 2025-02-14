import pytest

from app.models import Part
from app.tasks import import_parts_from_csv


@pytest.mark.django_db
def test_import_parts_from_csv():
    csv_content = (
        "part_number,name,details,price,quantity\n"
        "XPTO1234,Filtro de Óleo,Filtro de alta qualidade,45.00,50\n"
        "ABC123,Pastilha de Freio,Conjunto de 4 pastilhas,120.00,30\n"
    ).encode("utf-8")

    import_parts_from_csv(csv_content)

    assert Part.objects.count() == 2
    assert Part.objects.filter(part_number="XPTO1234").exists()
    assert Part.objects.filter(part_number="ABC123").exists()
