from django.contrib import admin

# Register your models here.
from app.models import CarModel, Part

admin.site.register(CarModel)
admin.site.register(Part)
