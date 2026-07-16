"""Регистрация и авторизация пользователей"""

import logging
import os

from decorators import handle_django_errors
from fastapi import APIRouter, Request
from schemas.user_schemas import NewUserRequest, NewUserResponse, TokenRequest, TokenResponse

from services.django_client import DjangoAPIClient

logger = logging.getLogger(__name__)
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
DJANGO_API_URL = os.getenv("DJANGO_API_URL")
django_client = DjangoAPIClient(DJANGO_API_URL)


@auth_router.post("/token", response_model=TokenResponse)
@handle_django_errors
async def login(request: Request, credentials: TokenRequest):
    logger.info(f"Авторизация пользователя {credentials.username}")
    path = "api/token/"  # base_url в джанго клиенте

    result = await django_client.request(
        method="POST", path=path, json=credentials.dict(), auth_token=None
    )

    return result


@auth_router.post("/register", response_model=NewUserResponse)
@handle_django_errors
async def register(request: Request, user_data: NewUserRequest):
    logger.info("Регистрация нового пользователя в системе...")

    path = "api/users/register/"
    result = await django_client.request(
        method="POST", path=path, json=user_data.dict(), auth_token=None
    )

    return result
