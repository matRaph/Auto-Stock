import django_filters.rest_framework
from django.contrib.auth.models import User
from rest_framework import permissions as django_permissions
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.models import CarModel, Part
from app.permissions import IsAdminUser, IsRegularUser
from app.serializers import CarModelSerializer, PartSerializer, UserSerializer

# Create your views here.


class PartViewset(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        "part_number": ["exact"],
        "name": ["exact"],
        "price": ["exact"],
        "quantity": ["exact"],
        "updated_at": ["exact"],
    }

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminUser | IsRegularUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        "name": ["exact"],
        "manufacturer": ["exact"],
        "year": ["exact"],
    }

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminUser | IsRegularUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


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
