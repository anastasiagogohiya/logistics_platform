import json
from datetime import datetime
import uuid
from .models import Order
from tariffs.models import Tariff
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    option_number = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'order_number', 'created_at', 'updated_at', 'client',
            'carrier', 'tariff', 'order_status',
            'factual_delivery_date', 'raw_data',
        ]

    def create(self, validated_data):
        option_id = validated_data.pop('option_number', None)
        if not option_id:
            raise serializers.ValidationError({"option_number": "Это поле обязательно"})

        try:
            tariff = Tariff.objects.get(id=option_id)
        except Tariff.DoesNotExist:
            raise serializers.ValidationError({"option_number": "Тариф не найден"})

        # Генерируем уникальный номер заказа
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        validated_data['order_number'] = order_number

        # Берём цену из запроса (или из тарифа, если не передана)
        price = validated_data.pop('price', getattr(tariff, 'price', 0.0))

        # Добавляем объекты связанных моделей
        validated_data['tariff'] = tariff
        validated_data['price'] = price
        validated_data['carrier'] = None  # или присвоить перевозчика из тарифа
        validated_data['raw_data'] = json.dumps({'option_number': option_id})

        # Все остальные поля (weight_kg, ship_from, ship_to, cargo_type и т.д.)
        # уже есть в validated_data, так как мы их передали из FastAPI

        return Order.objects.create(**validated_data)