from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .models import Carrier
from .serializers import CarrierSerializer


class CarrierViewSet(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]  # чтобы можно фильтровать в админке
    ordering_fields = "__all__"  # по всем полям можно сортировать
