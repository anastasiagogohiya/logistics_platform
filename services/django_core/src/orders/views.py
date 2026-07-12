from rest_framework import generics, permissions, viewsets
from .models import Order
from .serializers import OrderSerializer


# Вьхи по заказам

class OrderCreateView(generics.CreateAPIView):
    """Создание нового заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # заказ по option_number
    def perform_create(self, serializer):
        serializer.save(client=self.request.user,
                        order_number=self.request.data.get('option_number'))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]