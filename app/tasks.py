import csv
import io

from celery import shared_task

from .models import Part


@shared_task
def import_parts_from_csv(file_content):
    file = io.StringIO(file_content.decode("utf-8"))
    reader = csv.DictReader(file)

    parts_to_create = []
    for row in reader:
        part = Part(
            part_number=row["part_number"],
            name=row["name"],
            details=row["details"],
            price=float(row["price"]),
            quantity=int(row["quantity"]),
        )
        parts_to_create.append(part)

    Part.objects.bulk_create(parts_to_create)
