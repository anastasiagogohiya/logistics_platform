"""Заливка перевозчиков в БД"""
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from carriers.models import Carrier

class Command(BaseCommand):
    help = "Заливка перевозчиков в БД"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Заливка перевозчиков..."))
        carriers_data = [

            # ===== РОССИЯ =====
            {
                'name': 'ТрансЛогистик',
                'legal_name': 'ООО "ТрансЛогистик"',
                'country': 'Россия',
                'inn': '7701234567',
                'ogrn': '1027700123456',
                'reg_number': '',
                'address': 'г. Москва, ул. Транспортная, д. 10',
                'phone': '+7 (495) 123-45-67',
                'email': 'info@translogistic.ru',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'РосТрансГрупп',
                'legal_name': 'ООО "РосТрансГрупп"',
                'country': 'Россия',
                'inn': '7709876543',
                'ogrn': '1027709876543',
                'reg_number': '',
                'address': 'г. Москва, ул. Центральная, д. 1',
                'phone': '+7 (495) 012-34-56',
                'email': 'info@rostrans.ru',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'СПб-Экспресс',
                'legal_name': 'ООО "СПб-Экспресс"',
                'country': 'Россия',
                'inn': '7812345678',
                'ogrn': '1027801234567',
                'reg_number': '',
                'address': 'г. Санкт-Петербург, пр. Логистов, д. 5',
                'phone': '+7 (812) 234-56-78',
                'email': 'info@spbexpress.ru',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'РегионТранс',
                'legal_name': 'ООО "РегионТранс"',
                'country': 'Россия',
                'inn': '5501234567',
                'ogrn': '1025501234567',
                'reg_number': '',
                'address': 'г. Новосибирск, ул. Дальняя, д. 15',
                'phone': '+7 (383) 345-67-89',
                'email': 'info@regiontrans.ru',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'Дальний Восток Транс',
                'legal_name': 'ООО "ДВ Транс"',
                'country': 'Россия',
                'inn': '2501234567',
                'ogrn': '1022501234567',
                'reg_number': '',
                'address': 'г. Владивосток, ул. Портовая, д. 20',
                'phone': '+7 (423) 456-78-90',
                'email': 'info@dvtrans.ru',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'УралТрансСервис',
                'legal_name': 'ООО "УралТрансСервис"',
                'country': 'Россия',
                'inn': '6601234567',
                'ogrn': '1026601234567',
                'reg_number': '',
                'address': 'г. Екатеринбург, ул. Промышленная, д. 8',
                'phone': '+7 (343) 789-01-23',
                'email': 'info@uraltrans.ru',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'Волга-Транс',
                'legal_name': 'ООО "Волга-Транс"',
                'country': 'Россия',
                'inn': '5201234567',
                'ogrn': '1025201234567',
                'reg_number': '',
                'address': 'г. Нижний Новгород, ул. Речная, д. 12',
                'phone': '+7 (831) 890-12-34',
                'email': 'info@volgatrans.ru',
                'rating': 3,
                'is_active': True
            },
            {
                'name': 'СибирьЭкспресс',
                'legal_name': 'ООО "СибирьЭкспресс"',
                'country': 'Россия',
                'inn': '4201234567',
                'ogrn': '1024201234567',
                'reg_number': '',
                'address': 'г. Кемерово, ул. Кузбасская, д. 25',
                'phone': '+7 (384) 901-23-45',
                'email': 'info@sibexpress.ru',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'Юг-Транс',
                'legal_name': 'ООО "Юг-Транс"',
                'country': 'Россия',
                'inn': '2301234567',
                'ogrn': '1022301234567',
                'reg_number': '',
                'address': 'г. Краснодар, ул. Южная, д. 30',
                'phone': '+7 (861) 567-89-01',
                'email': 'info@ugtrans.ru',
                'rating': 3,
                'is_active': True
            },
            {
                'name': 'ЭкоЛогистик',
                'legal_name': 'ООО "ЭкоЛогистик"',
                'country': 'Россия',
                'inn': '5001234567',
                'ogrn': '1025001234567',
                'reg_number': '',
                'address': 'г. Москва, ул. Зеленая, д. 7',
                'phone': '+7 (498) 678-90-12',
                'email': 'info@ecologistik.ru',
                'rating': 5,
                'is_active': True
            },

            # ===== КИТАЙ =====
            {
                'name': 'China Logistics Group',
                'legal_name': 'China Logistics Group Co., Ltd.',
                'country': 'Китай',
                'inn': '',
                'ogrn': '',
                'reg_number': 'CN123456789',
                'address': 'Shanghai, Pudong New Area, Logistics Park, Building 15',
                'phone': '+86 (21) 1234-5678',
                'email': 'info@clg.cn',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'SinoTrans Express',
                'legal_name': 'SinoTrans International Logistics',
                'country': 'Китай',
                'inn': '',
                'ogrn': '',
                'reg_number': 'CN987654321',
                'address': 'Beijing, Daxing District, International Logistics Zone, 200m',
                'phone': '+86 (10) 8765-4321',
                'email': 'contact@sinotrans.cn',
                'rating': 4,
                'is_active': True
            },

            # ===== КАЗАХСТАН =====
            {
                'name': 'KazTrans Logistics',
                'legal_name': 'ТОО "KazTrans Logistics"',
                'country': 'Казахстан',
                'inn': '',
                'ogrn': '',
                'reg_number': 'KZ123456789',
                'address': 'г. Алматы, ул. Транспортная, д. 7, БЦ "Логистик"',
                'phone': '+7 (727) 234-56-78',
                'email': 'info@kaztrans.kz',
                'rating': 4,
                'is_active': True
            },

            # ===== БЕЛАРУСЬ =====
            {
                'name': 'БелТрансЭкспресс',
                'legal_name': 'ООО "БелТрансЭкспресс"',
                'country': 'Беларусь',
                'inn': '',
                'ogrn': '',
                'reg_number': 'BY123456789',
                'address': 'г. Минск, ул. Логистическая, д. 12',
                'phone': '+375 (17) 345-67-89',
                'email': 'info@beltrans.by',
                'rating': 4,
                'is_active': True
            },

            # ===== ГРУЗИЯ =====
            {
                'name': 'Georgian Logistics',
                'legal_name': 'LLC Georgian Logistics Group',
                'country': 'Грузия',
                'inn': '',
                'ogrn': '',
                'reg_number': 'GE123456789',
                'address': 'Tbilisi, Didube District, Transport Street, 45',
                'phone': '+995 (32) 234-56-78',
                'email': 'info@georgianlogistics.ge',
                'rating': 3,
                'is_active': True
            },

            # ===== ТУРЦИЯ =====
            {
                'name': 'Turkiye Nakliyat',
                'legal_name': 'Turkiye Nakliyat A.S.',
                'country': 'Турция',
                'inn': '',
                'ogrn': '',
                'reg_number': 'TR123456789',
                'address': 'Istanbul, Esenyurt, Logistics Center, Block C, No: 8',
                'phone': '+90 (212) 345-67-89',
                'email': 'info@turkiyenakliyat.com.tr',
                'rating': 4,
                'is_active': True
            }

        ]

        created_count = 0
        updated_count = 0

        for data in carriers_data:
            try:
                if data['country'] == 'Россия':
                    lookup_field = 'inn'
                    lookup_value = data['inn']
                else:
                    lookup_field = 'reg_number'
                    lookup_value = data['reg_number']

                carrier, created = Carrier.objects.get_or_create(
                    **{lookup_field: lookup_value},
                    defaults=data
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"Создан перевозчик {carrier.name} {carrier.country}")


                else:
                    # Обновляем данные
                    for key, value in data.items():
                        setattr(carrier, key, value)
                    carrier.save()
                    updated_count += 1
                    self.stdout.write(f'🔄 Обновлен: {carrier.name} ({carrier.country})')

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка при загрузке {data["name"]}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Непредвиденная ошибка: {e}'))

            self.stdout.write(self.style.SUCCESS(
                f'\nЗагрузка завершена! Создано: {created_count}, Обновлено: {updated_count}'))
            self.stdout.write(self.style.SUCCESS(f'Всего перевозчиков: {Carrier.objects.count()}'))
