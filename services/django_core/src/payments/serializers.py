# payments/serializers.py
from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "method",
            "status",
            "amount",
            "payment_url",
            "created_at",
            "paid_at",
        ]
        read_only_fields = ["id", "status", "payment_url", "created_at", "paid_at"]
