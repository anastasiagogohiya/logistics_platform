"""Схемы для валидации данных"""

from pydantic import BaseModel, Field

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
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    avatar: str | None = None
    is_staff: bool | None = None


# Ответ для одного пользователя
class UserResponse(BaseModel):
    user: UserBase


# Ответ для списка пользователей в системе
class UserListResponse(BaseModel):
    users: list[UserBase]


class NewUserRequest(BaseModel):
    """Пользователь предоставляет его данные"""

    username: str = Field(description="Имя пользователя", example="pipita")
    email: str | None = Field(None, description="Email", example="pipita@bk.ru")
    password: str = Field(description="Пароль", example="pipita123")
    first_name: str = Field(description="Имя", example="Pipita")
    last_name: str = Field(description="Фамилия", example="Ivanova")
    phone: str = Field(description="Телефон", example="89157655555")
    avatar: str | None = Field(None, description="Аватар", example="https://example.com/avatar.jpg")


class NewUserResponse(BaseModel):
    """Результат создания нового пользователя"""

    user: UserBase
