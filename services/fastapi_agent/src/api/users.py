import os
from fastapi import APIRouter, Request
from src.schemas.user_schemas import UserListResponse, UserResponse
import logging
from src.decorators import handle_django_errors
from src.utils.auth import extract_token
from src.services.django_client import DjangoAPIClient

logger = logging.getLogger(__name__)
user_router = APIRouter(prefix='/api/users', tags=['Users'])

DJANGO_API_URL = os.getenv("DJANGO_API_URL")
django_client = DjangoAPIClient(DJANGO_API_URL)

@user_router.get("/list", status_code=200,
                 response_model=UserListResponse,
                 summary="Получение списка всех пользователей")
@handle_django_errors
async def get_users(request: Request) -> UserListResponse:
    logger.info('Запрос на получение списка всех пользователей')
    auth_token = extract_token(request)
    result = await django_client.request(
        method="GET",
        path="/api/users/list/",
        auth_token=auth_token
    )
    return result  # соответствует UserListResponse

@user_router.get('/{id}', status_code=200,
                 response_model=UserResponse,
                 summary="Получение данных пользователя по id")
@handle_django_errors
async def get_user_info(request: Request, id: int) -> UserResponse:
    logger.info(f'Запрос на получение данных пользователя {id}')
    auth_token = extract_token(request)
    result = await django_client.request(
        method="GET",
        path=f"/api/users/{id}/",
        auth_token=auth_token
    )
    # Если Django возвращает объект пользователя без обёртки, а UserResponse ожидает поле "user"
    return {"user": result}