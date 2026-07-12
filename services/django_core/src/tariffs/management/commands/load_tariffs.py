"""Заливка тарифов в БД"""
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tariffs.models import Tariff
from carriers.models import Carrier
from orders.models import CargoChoice


class Command(BaseCommand):
    help = "Заливка тарифов в БД"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🚀 Заливка тарифов..."))

        # Получаем всех перевозчиков по имени
        carriers = {
            'ТрансЛогистик': Carrier.objects.get(name='ТрансЛогистик'),
            'РосТрансГрупп': Carrier.objects.get(name='РосТрансГрупп'),
            'СПб-Экспресс': Carrier.objects.get(name='СПб-Экспресс'),
            'РегионТранс': Carrier.objects.get(name='РегионТранс'),
            'Дальний Восток Транс': Carrier.objects.get(name='Дальний Восток Транс'),
            'УралТрансСервис': Carrier.objects.get(name='УралТрансСервис'),
            'Волга-Транс': Carrier.objects.get(name='Волга-Транс'),
            'СибирьЭкспресс': Carrier.objects.get(name='СибирьЭкспресс'),
            'Юг-Транс': Carrier.objects.get(name='Юг-Транс'),
            'ЭкоЛогистик': Carrier.objects.get(name='ЭкоЛогистик'),
            'China Logistics Group': Carrier.objects.get(name='China Logistics Group'),
            'SinoTrans Express': Carrier.objects.get(name='SinoTrans Express'),
            'KazTrans Logistics': Carrier.objects.get(name='KazTrans Logistics'),
            'БелТрансЭкспресс': Carrier.objects.get(name='БелТрансЭкспресс'),
            'Georgian Logistics': Carrier.objects.get(name='Georgian Logistics'),
            'Turkiye Nakliyat': Carrier.objects.get(name='Turkiye Nakliyat'),
        }

        tariffs_data = [
            # ==========================================
            # 1. ТрансЛогистик (Россия, Москва)
            # ==========================================
            {
                'carrier': carriers['ТрансЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Санкт-Петербург',
                'cargo_type': ['documents', 'package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 5000,
                'price_per_kg': 10,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },
            {
                'carrier': carriers['ТрансЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Санкт-Петербург',
                'cargo_type': ['documents', 'package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.EXPRESS,
                'price': 8000,
                'price_per_kg': 16,
                'delivery_days_min': 1,
                'delivery_days_max': 1,
                'is_active': True
            },
            {
                'carrier': carriers['ТрансЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Екатеринбург',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 15000,
                'price_per_kg': 15,
                'delivery_days_min': 4,
                'delivery_days_max': 6,
                'is_active': True
            },
            {
                'carrier': carriers['ТрансЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Новосибирск',
                'cargo_type': ['pallet', 'furniture', 'vehicle'],
                'cargo_weight_from': 100,
                'cargo_weight_to': 2000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 35000,
                'price_per_kg': 17.5,
                'delivery_days_min': 7,
                'delivery_days_max': 10,
                'is_active': True
            },

            # ==========================================
            # 2. РосТрансГрупп (Россия, Москва)
            # ==========================================
            {
                'carrier': carriers['РосТрансГрупп'],
                'ship_from': 'Москва',
                'ship_to': 'Краснодар',
                'cargo_type': ['package', 'pallet', 'liquid'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 800,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 12000,
                'price_per_kg': 15,
                'delivery_days_min': 3,
                'delivery_days_max': 5,
                'is_active': True
            },
            {
                'carrier': carriers['РосТрансГрупп'],
                'ship_from': 'Москва',
                'ship_to': 'Сочи',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.EXPRESS,
                'price': 20000,
                'price_per_kg': 40,
                'delivery_days_min': 2,
                'delivery_days_max': 2,
                'is_active': True
            },

            # ==========================================
            # 3. СПб-Экспресс (Россия, Санкт-Петербург)
            # ==========================================
            {
                'carrier': carriers['СПб-Экспресс'],
                'ship_from': 'Санкт-Петербург',
                'ship_to': 'Москва',
                'cargo_type': ['documents', 'package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 300,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 4500,
                'price_per_kg': 15,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },
            {
                'carrier': carriers['СПб-Экспресс'],
                'ship_from': 'Санкт-Петербург',
                'ship_to': 'Москва',
                'cargo_type': ['documents', 'package'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 100,
                'delivery_type': Tariff.DeliveryType.EXPRESS,
                'price': 7000,
                'price_per_kg': 70,
                'delivery_days_min': 1,
                'delivery_days_max': 1,
                'is_active': True
            },

            # ==========================================
            # 4. РегионТранс (Россия, Новосибирск)
            # ==========================================
            {
                'carrier': carriers['РегионТранс'],
                'ship_from': 'Новосибирск',
                'ship_to': 'Москва',
                'cargo_type': ['pallet', 'furniture', 'vehicle'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 30000,
                'price_per_kg': 20,
                'delivery_days_min': 6,
                'delivery_days_max': 8,
                'is_active': True
            },
            {
                'carrier': carriers['РегионТранс'],
                'ship_from': 'Новосибирск',
                'ship_to': 'Красноярск',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 8000,
                'price_per_kg': 16,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },

            # ==========================================
            # 5. Дальний Восток Транс (Россия, Владивосток)
            # ==========================================
            {
                'carrier': carriers['Дальний Восток Транс'],
                'ship_from': 'Владивосток',
                'ship_to': 'Москва',
                'cargo_type': ['container', 'vehicle', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 5000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 80000,
                'price_per_kg': 16,
                'delivery_days_min': 10,
                'delivery_days_max': 14,
                'is_active': True
            },
            {
                'carrier': carriers['Дальний Восток Транс'],
                'ship_from': 'Владивосток',
                'ship_to': 'Хабаровск',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 6000,
                'price_per_kg': 6,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },

            # ==========================================
            # 6. УралТрансСервис (Россия, Екатеринбург)
            # ==========================================
            {
                'carrier': carriers['УралТрансСервис'],
                'ship_from': 'Екатеринбург',
                'ship_to': 'Москва',
                'cargo_type': ['pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 14000,
                'price_per_kg': 14,
                'delivery_days_min': 4,
                'delivery_days_max': 5,
                'is_active': True
            },
            {
                'carrier': carriers['УралТрансСервис'],
                'ship_from': 'Екатеринбург',
                'ship_to': 'Тюмень',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 5000,
                'price_per_kg': 10,
                'delivery_days_min': 1,
                'delivery_days_max': 2,
                'is_active': True
            },

            # ==========================================
            # 7. Волга-Транс (Россия, Нижний Новгород)
            # ==========================================
            {
                'carrier': carriers['Волга-Транс'],
                'ship_from': 'Нижний Новгород',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'liquid'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 8000,
                'price_per_kg': 8,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },

            # ==========================================
            # 8. СибирьЭкспресс (Россия, Кемерово)
            # ==========================================
            {
                'carrier': carriers['СибирьЭкспресс'],
                'ship_from': 'Кемерово',
                'ship_to': 'Новосибирск',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 3000,
                'price_per_kg': 6,
                'delivery_days_min': 1,
                'delivery_days_max': 2,
                'is_active': True
            },

            # ==========================================
            # 9. Юг-Транс (Россия, Краснодар)
            # ==========================================
            {
                'carrier': carriers['Юг-Транс'],
                'ship_from': 'Краснодар',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 12000,
                'price_per_kg': 12,
                'delivery_days_min': 3,
                'delivery_days_max': 5,
                'is_active': True
            },
            {
                'carrier': carriers['Юг-Транс'],
                'ship_from': 'Краснодар',
                'ship_to': 'Сочи',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 300,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 4000,
                'price_per_kg': 13.3,
                'delivery_days_min': 1,
                'delivery_days_max': 2,
                'is_active': True
            },

            # ==========================================
            # 10. ЭкоЛогистик (Россия, Москва)
            # ==========================================
            {
                'carrier': carriers['ЭкоЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Санкт-Петербург',
                'cargo_type': ['documents', 'package'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 200,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 4000,
                'price_per_kg': 20,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },
            {
                'carrier': carriers['ЭкоЛогистик'],
                'ship_from': 'Москва',
                'ship_to': 'Казань',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 9000,
                'price_per_kg': 18,
                'delivery_days_min': 3,
                'delivery_days_max': 4,
                'is_active': True
            },

            # ==========================================
            # 11. China Logistics Group (Китай, Шанхай)
            # ==========================================
            {
                'carrier': carriers['China Logistics Group'],
                'ship_from': 'Шанхай',
                'ship_to': 'Москва',
                'cargo_type': ['container', 'pallet', 'vehicle'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 10000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 150000,
                'price_per_kg': 15,
                'delivery_days_min': 20,
                'delivery_days_max': 25,
                'is_active': True
            },
            {
                'carrier': carriers['China Logistics Group'],
                'ship_from': 'Шанхай',
                'ship_to': 'Владивосток',
                'cargo_type': ['container', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 8000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 80000,
                'price_per_kg': 10,
                'delivery_days_min': 10,
                'delivery_days_max': 14,
                'is_active': True
            },

            # ==========================================
            # 12. SinoTrans Express (Китай, Пекин)
            # ==========================================
            {
                'carrier': carriers['SinoTrans Express'],
                'ship_from': 'Пекин',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.EXPRESS,
                'price': 25000,
                'price_per_kg': 25,
                'delivery_days_min': 7,
                'delivery_days_max': 10,
                'is_active': True
            },

            # ==========================================
            # 13. KazTrans Logistics (Казахстан, Алматы)
            # ==========================================
            {
                'carrier': carriers['KazTrans Logistics'],
                'ship_from': 'Алматы',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 2000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 30000,
                'price_per_kg': 15,
                'delivery_days_min': 5,
                'delivery_days_max': 7,
                'is_active': True
            },
            {
                'carrier': carriers['KazTrans Logistics'],
                'ship_from': 'Алматы',
                'ship_to': 'Астана',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 10000,
                'price_per_kg': 10,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },

            # ==========================================
            # 14. БелТрансЭкспресс (Беларусь, Минск)
            # ==========================================
            {
                'carrier': carriers['БелТрансЭкспресс'],
                'ship_from': 'Минск',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'liquid'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 12000,
                'price_per_kg': 12,
                'delivery_days_min': 2,
                'delivery_days_max': 3,
                'is_active': True
            },
            {
                'carrier': carriers['БелТрансЭкспресс'],
                'ship_from': 'Минск',
                'ship_to': 'Санкт-Петербург',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 800,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 10000,
                'price_per_kg': 12.5,
                'delivery_days_min': 3,
                'delivery_days_max': 4,
                'is_active': True
            },

            # ==========================================
            # 15. Georgian Logistics (Грузия, Тбилиси)
            # ==========================================
            {
                'carrier': carriers['Georgian Logistics'],
                'ship_from': 'Тбилиси',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'furniture'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 20000,
                'price_per_kg': 20,
                'delivery_days_min': 5,
                'delivery_days_max': 7,
                'is_active': True
            },
            {
                'carrier': carriers['Georgian Logistics'],
                'ship_from': 'Тбилиси',
                'ship_to': 'Батуми',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 500,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 5000,
                'price_per_kg': 10,
                'delivery_days_min': 1,
                'delivery_days_max': 2,
                'is_active': True
            },

            # ==========================================
            # 16. Turkiye Nakliyat (Турция, Стамбул)
            # ==========================================
            {
                'carrier': carriers['Turkiye Nakliyat'],
                'ship_from': 'Стамбул',
                'ship_to': 'Москва',
                'cargo_type': ['package', 'pallet', 'container'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 2000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 35000,
                'price_per_kg': 17.5,
                'delivery_days_min': 7,
                'delivery_days_max': 10,
                'is_active': True
            },
            {
                'carrier': carriers['Turkiye Nakliyat'],
                'ship_from': 'Стамбул',
                'ship_to': 'Анкара',
                'cargo_type': ['package', 'pallet'],
                'cargo_weight_from': 0,
                'cargo_weight_to': 1000,
                'delivery_type': Tariff.DeliveryType.STANDARD,
                'price': 8000,
                'price_per_kg': 8,
                'delivery_days_min': 1,
                'delivery_days_max': 2,
                'is_active': True
            },
        ]

        created_count = 0
        skipped_count = 0

        for data in tariffs_data:
            try:
                tariff, created = Tariff.objects.get_or_create(
                    carrier=data['carrier'],
                    ship_from=data['ship_from'],
                    ship_to=data['ship_to'],
                    cargo_weight_from=data['cargo_weight_from'],
                    cargo_weight_to=data['cargo_weight_to'],
                    delivery_type=data['delivery_type'],
                    defaults=data
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f'✅ Создан тариф: {tariff.carrier.name} - {tariff.ship_from} → {tariff.ship_to} ({tariff.get_delivery_type_display()})')
                else:
                    skipped_count += 1
                    self.stdout.write(
                        f'⏭️ Тариф уже существует: {tariff.carrier.name} - {tariff.ship_from} → {tariff.ship_to}')

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка при загрузке тарифа: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Непредвиденная ошибка: {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Загрузка завершена! Создано: {created_count}, Пропущено: {skipped_count}'
        ))
        self.stdout.write(self.style.SUCCESS(f'📊 Всего тарифов: {Tariff.objects.count()}'))