from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .services.payment_gateway import PaymentGateway


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        # При создании платежа вызываем шлюз и сохраняем полученные данные
        payment_data = PaymentGateway.create_payment(amount=serializer.validated_data.get('amount'))
        serializer.save(
            payment_id=payment_data['payment_id'],
            payment_url=payment_data['payment_url'],
            status=payment_data['status']
        )

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Имитация оплаты: подтверждаем платёж через шлюз."""
        payment = self.get_object()
        if payment.status == Payment.Status.PAID:
            return Response({'detail': 'Платёж уже оплачен'}, status=status.HTTP_400_BAD_REQUEST)

        # Вызываем шлюз для подтверждения
        result = PaymentGateway.confirm_payment(payment.payment_id)

        # Обновляем статус
        payment.status = result['status']
        payment.paid_at = result.get('paid_at')
        payment.save()

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)