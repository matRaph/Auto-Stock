from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"parts", views.PartViewset, basename="part")
router.register(r"car-models", views.CarModelViewSet, basename="car_model")
router.register(r"user-register", views.RegisterView, basename="user_register")
router.register(r"import-parts", views.ImportPartsFromCSVViewSet, basename="import_parts")

urlpatterns = [
    path("", include(router.urls)),
]
