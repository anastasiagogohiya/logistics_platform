from typing import List, Optional
from src.schemas.tariff_schemas import TariffOption
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1, alias="message", description="Текст запроса пользователя")
    session_id: str = Field(..., description="Уникальный идентификатор сессии для хранения разговора")

    class Config:
        populate_by_name = True  # разрешает использовать оба имени text и message

    @field_validator('text')
    def validate_text(cls, v: str) -> str:
        # Удаляем пробелы в начале и конце
        stripped = v.strip()
        if not stripped:
            raise ValueError('Введите, пожалуйста, текст запроса на перевозку!')
        return stripped


class ChatResponse(BaseModel):
    parsed: dict                          # распознанные сущности
    offers: List[TariffOption]            # список тарифов (можно использовать тип TariffOption)
    message: str                          # человекочитаемое сообщение
    need_clarification: bool = False      # требуется ли уточнение