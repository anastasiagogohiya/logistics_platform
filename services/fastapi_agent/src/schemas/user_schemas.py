"""Схемы для валидации данных"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal


"""
Пока не решила какая должны быть регистрация
через номер телефона или emai или еще как
не сделала валидация полей"""

class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str

# Базовый класс для переиспользования
class UserBase(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    is_staff: Optional[bool] = None

# Ответ для одного пользователя
class UserResponse(BaseModel):
    user: UserBase

# Ответ для списка пользователей в системе
class UserListResponse(BaseModel):
    users: List[UserBase]

class NewUserRequest(BaseModel):
    """Пользователь предоставляет его данные"""
    username: str = Field(..., example='pipita')
    email: Optional[str] = Field(None, example='pipita@bk.ru')
    password: str = Field(..., example='pipita123')
    first_name: str = Field(..., example='Pipita')
    last_name: str = Field(..., example='Ivanova')
    phone: str = Field(..., example='89157655555')
    avatar: Optional[str] = Field(None, example="https://example.com/avatar.jpg")


class NewUserResponse(BaseModel):
    """Результат создания нового пользователя"""
    user: UserBase
