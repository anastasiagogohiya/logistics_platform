from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.tariff_selector import TariffSelector
from rest_framework.filters import OrderingFilter
from .models import Tariff
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import TariffSerializer
from rest_framework.decorators import permission_classes

# Фастапи отправляет запрос на поиск тарифа
# Поиск тарифов
# Резервирование тарифа
# Подтверждение выбора

@api_view(['POST'])
@permission_classes([AllowAny])
def search_tariff(request):
    """Поиск тарифа по параметрам отправленным клиентом"""
    selector = TariffSelector()

    tariffs = selector.find_available_tariff(
        ship_from=request.data.get('ship_from'),
        ship_to=request.data.get('ship_to'),
        cargo_type=request.data.get('cargo_type'),
        weight_kg=request.data.get('weight_kg'),
        delivery_type=request.data.get('delivery_type', 'standard'), # по умолчанию стандарт если не указано другое
        is_hazardous=request.data.get('is_hazardous', False)
    )

    if not tariffs:
        return Response({
            'success': False,
            'message': '😔 По вашему запросу ничего не найдено. Попробуйте изменить параметры.',
            'found': 0,
            'results': [],
            'response_type': 'empty'
        })

    results = []

    for idx, tariff in enumerate(tariffs[:5], start=1):
        results.append({
            'option_number': idx,
            'tariff_id': tariff.id,
            'carrier_name': tariff.carrier.name,
            'carrier_rating': tariff.carrier.rating,
            'price': float(tariff.price),
            'delivery_days': tariff.delivery_days_min, # берем мин. срок
            'ship_from': tariff.ship_from,
            'ship_to': tariff.ship_to,
            'cargo_types': tariff.cargo_type,
            'weight_range': f"{tariff.cargo_weight_from}-{tariff.cargo_weight_to} кг",
            'is_express': tariff.delivery_type == 'express'
        })

    return Response({
        'success': True,
        'found': len(results),
        'results': results,
        'response_type': 'success'
    })


class TariffViewSet(viewsets.ModelViewSet):
    """Общий список активных тарифов в системе"""
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter] # чтобы можно фильтровать в админке
    ordering_fields = '__all__'  # по всем полям можно сортировать