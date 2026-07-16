"""Схемы для валидации данных"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TariffSearchRequest(BaseModel):
    """Запрос на поиск тарифов с обязательной проверкой"""

    ship_from: str | None = Field(
        default=None,
        description="Откуда везти",
        examples=["Москва"],  # 👈 examples (множественное число)
    )
    ship_to: str | None = Field(default=None, description="Куда везти", examples=["Казань"])
    cargo_type: str | None = Field(default=None, description="Что везем", examples=["furniture"])
    weight_kg: float | None = Field(default=None, description="Вес в кг", examples=[50.0])
    shipment_date: date | None = Field(
        default=None,
        description="Дата отгрузки (YYYY-MM-DD) - опционально",
        examples=["2026-07-01"],
    )
    delivery_type: Literal["standard", "express"] = Field(
        default="standard", description="Тип доставки"
    )
    is_hazardous: bool = Field(default=False, description="Опасный груз")
    quantity: int = Field(default=1, ge=1, description="Количество мест", examples=[1])

    @field_validator("ship_from", "ship_to", "cargo_type", "weight_kg")
    def check_required_fields(cls, v, info):
        if v is None or (isinstance(v, str) and not v.strip()):
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"Пожалуйста, укажите {field_name}") from None
        return v

    @field_validator("weight_kg")
    def validate_weight(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Вес должен быть больше 0") from None
        if v is not None and v > 100000:
            raise ValueError("Вес не может превышать 100 000 кг") from None
        return v

    @field_validator("shipment_date", mode="before")
    def validate_shipment_date(cls, v):
        if v is None:
            return v
        if isinstance(v, date):
            if v < date.today():
                raise ValueError("Дата отгрузки не может быть в прошлом") from None
            return v
        if isinstance(v, str):
            try:
                shipment_date = datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD") from None
            if shipment_date < date.today():
                raise ValueError("Дата отгрузки не может быть в прошлом") from None
            return shipment_date
        raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD") from None


class TariffOption(BaseModel):
    """Компактный вариант тарифа для бота"""

    option_number: int = Field(description="Номер для выбора", examples=[1])
    tariff_id: int = Field(description="ID для создания заказа", examples=[123])
    carrier_name: str = Field(description="Перевозчик", examples=["ЭкоЛогистик"])
    price: float = Field(description="Цена, ₽", examples=[9000.0])
    delivery_days: int = Field(description="Срок, дней", examples=[3])
    is_express: bool = Field(default=False, description="Экспресс-доставка")


class TariffSearchResponse(BaseModel):
    """Ответ клиенту после поиска тарифов"""

    success: bool = Field(description="Успешность запроса", examples=[True])
    message: str | None = Field(
        default=None, description="Текст для бота (опционально)", examples=["Найдено 3 варианта"]
    )
    found: int = Field(description="Количество вариантов", examples=[3])
    results: list[TariffOption] = Field(
        default_factory=list, description="Список вариантов для выбора"
    )
    debug_info: dict | None = Field(
        default=None, description="Дополнительная информация (для разработчиков)"
    )
    response_type: Literal["success", "empty", "error"] = Field(
        default="success", description="Тип ответа", examples=["success"]
    )
