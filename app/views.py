import django_filters.rest_framework
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions as django_permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from app.models import CarModel, Part
from app.permissions import IsAdminUser, IsRegularUser
from app.serializers import (
    CarModelDetailSerializer,
    CarModelSerializer,
    PartDetailSerializer,
    PartSerializer,
    UserSerializer,
    VinculoParteSerializer,
)

from .tasks import import_parts_from_csv

# Create your views here.


class PartViewset(viewsets.ModelViewSet):
    queryset = Part.objects.all()

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        "part_number": ["exact"],
        "name": ["exact"],
        "price": ["exact"],
        "quantity": ["exact"],
        "updated_at": ["exact"],
    }

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PartDetailSerializer
        return PartSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminUser | IsRegularUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        "name": ["exact"],
        "manufacturer": ["exact"],
        "year": ["exact"],
    }

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CarModelDetailSerializer
        if self.action == "vincular_parte":
            return VinculoParteSerializer
        if self.action == "desvincular_parte":
            return VinculoParteSerializer
        return CarModelSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminUser | IsRegularUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["patch"])
    def vincular_parte(self, request, pk):
        car_model = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.vincular_parte(car_model)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def desvincular_parte(self, request, pk):
        car_model = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.desvincular_parte(car_model)
        return Response(status=status.HTTP_200_OK)


class RegisterView(viewsets.ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [django_permissions.AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImportPartsFromCSVViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAdminUser]  # Somente administradores podem fazer upload

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Arquivo CSV contendo as peças",
            )
        ],
    )
    def create(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Nenhum arquivo enviado"}, status=status.HTTP_400_BAD_REQUEST)

        file_content = file.read()

        # Chama a tarefa Celery para processar o CSV de forma assíncrona
        import_parts_from_csv.delay(file_content)

        return Response({"status": "Arquivo recebido e processamento iniciado"}, status=status.HTTP_202_ACCEPTED)
