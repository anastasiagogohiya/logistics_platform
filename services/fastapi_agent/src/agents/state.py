import logging
from datetime import date
from typing import Any

from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


class DialogState(BaseModel):
    """Состояние диалога, синхронизируемое с Redis."""

    current_message: str | None = None  # последнее сообщение пользователя
    raw_text: str | None = None
    response_message: str | None = None  # для ответов пользователю
    auth_token: str | None = None

    # Поля, собираемые от пользователя
    ship_from: str | None = None
    ship_to: str | None = None
    cargo_type: str = "other"
    delivery_type: str | None = "standard"  # если не указал то по умолчанию standard
    weight_kg: float | None = None
    quantity: int | None = 1  # если не указал то по умолчанию 1
    is_hazardous: bool = False  # если не указал по умолчанию не опасный
    shipment_date: date | None = None

    # Результаты поиска
    offers: list[dict[str, Any]] = []
    selected_offer: dict[str, Any] | None = None
    order_number: str | None = None  # если оформлен заказ

    payment_id: int | None = None
    payment_method: str = "prepaid"  # или отдельная модель
    payment_url: str | None = None

    # Управление диалогом
    step: str = "init"  # init, collecting, searching, choosing, confirming, done, error
    error_message: str | None = None

    logger.info("DialogState инициализирован")

    # Простая базовая валидация данных
    @field_validator("weight_kg")
    def validate_weight(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Вес должен быть больше 0")
        return v

    @field_validator("quantity")
    def validate_quantity(cls, v):
        if v is not None and v < 1:
            raise ValueError("Количество мест должно быть не менее 1")
        return v

    @field_validator("shipment_date")
    def validate_date(cls, v):
        if v is not None and v < date.today():
            raise ValueError("Дата отправки не может быть в прошлом")
        return v
