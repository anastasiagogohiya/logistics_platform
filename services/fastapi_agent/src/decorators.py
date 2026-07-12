# App.tsx/decorators.py
import logging
from functools import wraps
from fastapi import HTTPException
import httpx

logger = logging.getLogger(__name__)


def handle_django_errors(func):
    """Декоратор для обработки ошибок при запросах к Django"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Ошибка HTTP: {e.response.status_code} - {e.response.text[:200]}")
            raise HTTPException(status_code=e.response.status_code, detail="Ошибка в Django")
        except httpx.ConnectError:
            logger.error("❌ Django сервер недоступен")
            raise HTTPException(status_code=504, detail="Сервис временно недоступен")
        except httpx.TimeoutException:
            logger.error("❌ Таймаут при запросе к Django")
            raise HTTPException(status_code=504, detail="Сервис не отвечает")
        except Exception as e:
            logger.error(f"❌ Неизвестная ошибка: {type(e).__name__} - {str(e)}")
            raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return wrapper