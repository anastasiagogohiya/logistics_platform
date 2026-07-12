# src/services/django_client.py
import httpx
import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class APIEndpoints:
    SEARCH_TARIFFS = "/api/tariffs/search/"
    CREATE_ORDER = "/api/orders/"
    CREATE_PAYMENT = "/api/payments/"


class DjangoAPIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Запрос по API с заголовком авторизации"""

        logger.info(f"🚀 Запрос к {path}...")
        url = urljoin(self.base_url + '/', path.lstrip('/'))
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"  # или "Token", смотрите как в Django

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.request(method, url, data=data, json=json, headers=headers)
            if resp.status_code >= 400:
                logger.error(f"❌ Ошибка {resp.status_code} при запросе к {url}")
                logger.error(f"📄 Тело ответа: {resp.text}")
                logger.error(f"📤 Отправленные данные: {json or data}")
            resp.raise_for_status()
            return resp.json()


    async def search_tariffs(self, params, auth_token: Optional[str] = None) -> Dict[str, Any]:
        return await self.request("POST", APIEndpoints.SEARCH_TARIFFS, json=params, auth_token=auth_token)


    async def create_order(self, order_data, auth_token: Optional[str] = None) -> Dict[str, Any]:
        return await self.request("POST", APIEndpoints.CREATE_ORDER, json=order_data, auth_token=auth_token)

    async def create_payment(self, payment_data, auth_token=None):
        return await self.request("POST", APIEndpoints.CREATE_PAYMENT, json=payment_data, auth_token=auth_token)

    async def pay_payment(self, payment_id: int, auth_token: Optional[str] = None) -> Dict[str, Any]:
        """Вызов эндпоинта для подтверждения оплаты."""
        return await self.request("POST", f"/api/payments/{payment_id}/pay/", auth_token=auth_token)