# Create your models here.
from django.db import models


class Part(models.Model):
    part_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    details = models.TextField(
        null=True,
        blank=True,
    )
    price = models.FloatField()
    quantity = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    car_model = models.ManyToManyField("CarModel", related_name="parts")

    def __str__(self):
        return f"{self.part_number} - {self.name}"


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.manufacturer} - {self.name} - {self.year}"
