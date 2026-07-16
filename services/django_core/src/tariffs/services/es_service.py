import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Q, Search

from ..models import Tariff

"""Короче код, удобно писать elasticsearch-dsl"""


class ElasticsearchService:
    def __init__(self):
        host = os.getenv("ELASTICSEARCH_HOST", "localhost")
        port = os.getenv("ELASTICSEARCH_PORT", "9200")
        self.client = Elasticsearch([f"http://{host}:{port}"])  # подключение
        self.index_name = "tariffs"

    def create_index(self):
        index = Index(self.index_name, self.client)
        # Настройки для русского языка
        index.settings(number_of_shards=1, number_of_replicas=0)

        # Создаем
        if not index.exists():
            index.create()

    def index_tariff(self, tariff):
        """Отправляем один тариф в Elasticsearch"""
        doc = {
            "id": tariff.id,
            "ship_from": tariff.ship_from,
            "ship_to": tariff.ship_to,
            "cargo_type": tariff.cargo_type,
            "weight_from": tariff.cargo_weight_from,
            "weight_to": tariff.cargo_weight_to,
            "delivery_type": tariff.delivery_type,
            "price": float(tariff.price),
            "is_active": tariff.is_active,
            "carrier_rating": tariff.carrier.rating if tariff.carrier else 0,
        }

        # Отправляем в ES
        self.client.index(index=self.index_name, id=tariff.id, body=doc)

    def search(
        self,
        ship_from=None,
        ship_to=None,
        cargo_type=None,
        weight_kg=None,
        delivery_type=None,
        is_hazardous=False,
    ):
        """Поиск тарифов по параметрам"""

        # 1. Создаем поиск
        search = Search(using=self.client, index=self.index_name)

        # 2. Собираем условия
        conditions = []

        # Поиск городу отправки, не точное совпадение
        if ship_from:
            conditions.append(Q("match", ship_from={"query": ship_from, "fuzziness": "AUTO"}))

        if ship_to:
            conditions.append(Q("match", ship_to={"query": ship_to, "fuzziness": "AUTO"}))

        if cargo_type:
            conditions.append(Q("match", cargo_type={"query": cargo_type, "fuzziness": "AUTO"}))

        if delivery_type:
            conditions.append(Q("term", delivery_type=delivery_type))

        # Поиск по весу: weight_kg должен быть в диапазоне
        if weight_kg is not None:  # вес клиента
            conditions.append(
                Q("range", weight_from={"lte": weight_kg})  # от <= вес клиента
            )
            conditions.append(
                Q("range", weight_to={"gte": weight_kg})  # до >= вес клиента
            )

        if is_hazardous:
            conditions.append(Q("term", is_hazardous=True))

        # 3. Применяем все условия
        if conditions:
            search = search.query(Q("bool", must=conditions))

        # 4. Только активные тарифы
        search = search.filter("term", is_active=True)

        # 5. Ограничиваем количество
        search = search.extra(size=100)

        # 6. Возвращаем только ID
        search = search.source(["id"])

        # 7. Выполняем
        response = search.execute()

        # 8. Извлекаем ID
        tariff_ids = [hit.id for hit in response]

        return tariff_ids

    def delete_tariff(self, tariff_id):
        """Удалить тариф из Elasticsearch"""
        self.client.delete(index=self.index_name, id=tariff_id, ignore=[404])  # type: ignore

    def reindex_all(self):
        """Залить все тарифы из БД в Elasticsearch (один раз)"""

        tariffs = Tariff.objects.select_related("carrier").all()

        for tariff in tariffs:
            self.index_tariff(tariff)
