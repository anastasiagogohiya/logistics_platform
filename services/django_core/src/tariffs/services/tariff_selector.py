from ..models import Tariff
from .es_service import ElasticsearchService

# Для быстрого и оптимизированного поиска тарифов Elasticsearch + POstgres из этого файла будет запросы в сервис

# в этом файле (бизнес-логика подбора)

# Логика подбора перевозчика, тарифа, срока доставки:
# Подбор будет по:
# 1. направлению (от ... до)
# 2. по типу груза -> Тип груза определяет вид транспорта
# 3. по весу, объему
# 4. по срокам доставки
# 5. по цене
# 6. по рейтингу


class TariffSelector:
    def __init__(self):
        self.es_service = ElasticsearchService()

    def find_available_tariff(self, ship_from, ship_to,
                         cargo_type, weight_kg, delivery_type,
                         is_hazardous=False):

        # Шаг 1: Поиск в ES (только ID)
        tariff_ids = self.es_service.search(
            ship_from=ship_from,
            ship_to=ship_to,
            cargo_type=cargo_type,
            weight_kg=weight_kg,
            delivery_type=delivery_type,
            is_hazardous=is_hazardous
        )

        # Шаг 2: Получение из PG
        tariffs = Tariff.objects.filter(
            id__in=tariff_ids,
            is_active=True
        ).select_related('carrier')

        # Шаг 3: Бизнес-логика
        tariffs = self._apply_carrier_rating_filter(tariffs)
        tariffs = self._apply_discounts(tariffs, weight_kg)

        # Шаг 4: Сортировка
        return tariffs.order_by('price', '-carrier__rating')

    def _apply_carrier_rating_filter(self, tariffs):
        """Фильтр по рейтингу перевозчика исключаем перевозчиков с рейтингом меньше 3"""
        return tariffs.filter(carrier__rating__gte=3)

    def _apply_discounts(self, tariffs, weight_kg):
        """Применение скидок (Пока нет скидок)"""
        return tariffs
