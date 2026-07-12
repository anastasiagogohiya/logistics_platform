"""Схемы для валидации данных"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal
from datetime import date, datetime

# Пользователь в запросе обязательно указывает:
# откуда везти, куда вести
# что везти cargo_type
# вес

# опциональные, необязательные поля
# если клиент сразу не указал что доставка срочная, то по умолчанию стандартная
class TariffSearchRequest(BaseModel):
    """Запрос на поиск тарифов с обязательной проверкой"""

    ship_from: Optional[str] = Field(default=None,
                                     description="Откуда везти",
                                     example='Москва')
    ship_to: Optional[str] = Field(default=None,
                                   description="Куда везти",
                                   example='Казань')
    cargo_type: Optional[str] = Field(default=None,
                                      description="Что везем",
                                      example='furniture')
    weight_kg: Optional[float] = Field(default=None,
                                       description="Вес в кг",
                                       example=50)
    shipment_date: Optional[date] = Field(
        default=None,
        description="Дата отгрузки (YYYY-MM-DD) - опционально",
        example="2026-07-01"
    )
    delivery_type: Literal['standard', 'express'] = Field(
        default='standard',
        description="Тип доставки"
    )
    is_hazardous: bool = Field(default=False)
    quantity: int = Field(default=1, ge=1, description="Количество мест")
    #dimensions: Optional[str] = Field(
    #    default=None,
    #    description="Габариты (ДхШхВ)",
    #    example="100x80x50"
    #)

    # ✅ V2 валидация
    @field_validator('ship_from', 'ship_to', 'cargo_type', 'weight_kg')
    def check_required_fields(cls, v, info):
        if v is None or (isinstance(v, str) and not v.strip()):
            field_name = info.field_name.replace('_', ' ')
            raise ValueError(f'Пожалуйста, укажите {field_name}')
        return v

    @field_validator('weight_kg')
    def validate_weight(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Вес должен быть больше 0')
        if v is not None and v > 100000:
            raise ValueError('Вес не может превышать 100 000 кг')
        return v

@field_validator('shipment_date', mode='before')
def validate_shipment_date(cls, v):
    if v is None:
        return v  # если допускается null
    if isinstance(v, date):
        # Если уже объект date (например, пришло из другого источника)
        if v < date.today():
            raise ValueError('Дата отгрузки не может быть в прошлом')
        return v
    if isinstance(v, str):
        try:
            # Парсим строку формата YYYY-MM-DD
            shipment_date = datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Неверный формат даты. Используйте YYYY-MM-DD')
        if shipment_date < date.today():
            raise ValueError('Дата отгрузки не может быть в прошлом')
        return shipment_date
    raise ValueError('Неверный формат даты. Используйте YYYY-MM-DD')

class TariffOption(BaseModel):
    """Компактный вариант тарифа для бота"""
    option_number: int = Field(..., description="Номер для выбора")
    tariff_id: int = Field(..., description="ID для создания заказа")
    carrier_name: str = Field(..., description="Перевозчик")
    price: float = Field(..., description="Цена, ₽")
    delivery_days: int = Field(..., description="Срок, дней")
    is_express: bool = Field(default=False)

    # Расчетная дата доставки исходя из delivery days

class TariffSearchResponse(BaseModel):
    """Ответ клиенту после поиска тарифов"""
    success: bool
    message: Optional[str] = Field(
        default=None,  # Необязательное поле
        description="Текст для бота (опционально)"
    )
    found: int = Field(..., description="Количество вариантов")
    results: List[TariffOption] = Field(
        default_factory=list,
        description="Список вариантов для выбора"
    )

    # Дополнительные поля для отладки
    debug_info: Optional[dict] = Field(
        default=None,
        description="Дополнительная информация (для разработчиков)"
    )

    # Тип ответа для бота
    response_type: Literal['success', 'empty', 'error'] = Field(
        default='success',
        description="Тип ответа"
    )
