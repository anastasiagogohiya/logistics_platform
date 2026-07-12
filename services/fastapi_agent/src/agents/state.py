from typing import Optional, List, Dict, Any
from datetime import date
from pydantic import BaseModel, field_validator
import logging

logger = logging.getLogger(__name__)

class DialogState(BaseModel):
    """Состояние диалога, синхронизируемое с Redis."""
    current_message: Optional[str] = None  # последнее сообщение пользователя
    raw_text: Optional[str] = None
    response_message: Optional[str] = None  # для ответов пользователю
    auth_token: Optional[str] = None

    # Поля, собираемые от пользователя
    ship_from: Optional[str] = None
    ship_to: Optional[str] = None
    cargo_type: str = "other"
    delivery_type: Optional[str] = "standard" # если не указал то по умолчанию standard
    weight_kg: Optional[float] = None
    quantity: Optional[int] = 1  # если не указал то по умолчанию 1
    is_hazardous: bool = False  # если не указал по умолчанию не опасный
    shipment_date: Optional[date] = None

    # Результаты поиска
    offers: List[Dict[str, Any]] = []
    selected_offer: Optional[Dict[str, Any]] = None
    order_number: Optional[str] = None # если оформлен заказ

    payment_id: Optional[int] = None
    payment_method: str = "prepaid"  # или отдельная модель
    payment_url: Optional[str] = None

    # Управление диалогом
    step: str = "init"  # init, collecting, searching, choosing, confirming, done, error
    error_message: Optional[str] = None

    logger.info("DialogState инициализирован")

    # Простая базовая валидация данных
    @field_validator('weight_kg')
    def validate_weight(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Вес должен быть больше 0')
        return v

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v is not None and v < 1:
            raise ValueError('Количество мест должно быть не менее 1')
        return v

    @field_validator('shipment_date')
    def validate_date(cls, v):
        if v is not None and v < date.today():
            raise ValueError('Дата отправки не может быть в прошлом')
        return v