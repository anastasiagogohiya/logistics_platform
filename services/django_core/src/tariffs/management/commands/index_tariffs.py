from django.core.management.base import BaseCommand
from tariffs.services.es_service import ElasticsearchService


class Command(BaseCommand):
    help = "Индексация всех тарифов в Elasticsearch"

    def handle(self, *args, **options):
        self.stdout.write("Начинаю индексацию...")

        es_service = ElasticsearchService()

        # Создаем индекс
        es_service.create_index()
        self.stdout.write("Индекс создан")

        # Заливаем данные
        es_service.reindex_all()
        self.stdout.write("Все тарифы залиты в Elasticsearch")
