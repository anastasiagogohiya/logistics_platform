"""Схемы для валидации данных"""

from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    option_number: int = Field(description="номер выбранного тарифа", examples=[1])


class OrderCreateResponse(BaseModel):
    id: int | None = None  # если Django возвращает первичный ключ
    order_number: str = Field(description="Уникальный номер заказа")
    client: int = Field(description="ID клиента (пользователя)")
    created_at: datetime = Field(description="Дата создания заказа")
    updated_at: datetime | None = Field(None, description="Дата последнего обновления")

    cargo_type: str = Field(description="Тип груза (выбор из CargoChoice)")
    weight_kg: float = Field(description="Вес в кг")
    dimensions: str | None = Field(None, description="Габариты (строка)")
    quantity: int = Field(description="Количество мест")
    is_hazardous: bool = Field(description="Опасный груз?")

    ship_from: str = Field(description="Адрес отправления")
    ship_to: str = Field(description="Адрес назначения")
    requested_delivery_date: datetime = Field(description="Желаемая дата доставки")
    delivery_type: str = Field(description="Тип доставки (standard/express)")

    carrier: int | None = Field(None, description="ID назначенного перевозчика (может быть null)")
    tariff: int | None = Field(None, description="ID выбранного тарифа (может быть null)")
    price: float | None = Field(None, description="Цена перевозки (может быть null)")

    order_status: str = Field(description="Текущий статус заказа")
    expected_delivery_date: datetime | None = Field(
        None, description="Ожидаемая дата доставки (рассчитанная)"
    )
    factual_delivery_date: datetime | None = Field(None, description="Фактическая дата доставки")

    class Config:
        # Позволяет использовать примеры из модели, если нужно
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_number": "ORD-2026-001",
                "client": 42,
                "created_at": "2026-07-07T10:00:00",
                "updated_at": None,
                "cargo_type": "documents",
                "weight_kg": 5.2,
                "dimensions": "30x20x10",
                "quantity": 1,
                "is_hazardous": False,
                "ship_from": "Moscow",
                "ship_to": "Saint Petersburg",
                "requested_delivery_date": "2026-07-10T18:00:00",
                "delivery_type": "standard",
                "carrier": None,
                "tariff": 3,
                "price": 1500.00,
                "order_status": "created",
                "expected_delivery_date": "2026-07-11T12:00:00",
                "factual_delivery_date": None,
            }
        }
