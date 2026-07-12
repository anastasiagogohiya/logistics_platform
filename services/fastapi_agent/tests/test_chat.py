# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app
import uuid
from langgraph.checkpoint.memory import MemorySaver  # 🔥 ИСПРАВЛЕНО


def test_full_dialog(auth_client):
    """Тест с синхронным MemorySaver."""

    # 🔥 Используем синхронный MemorySaver
    with patch('src.agents.checkpointer.get_redis_checkpointer') as mock_redis:
        mock_redis.return_value = MemorySaver()

        session_id = f"test-{uuid.uuid4().hex[:8]}"

        # Мокаем Django вызовы
        mock_offers = {
            "results": [{
                "option_number": 1,
                "tariff_id": 20,
                "carrier_name": "ТестПеревозчик",
                "carrier_rating": 5,
                "price": 9000.0,
                "delivery_days": 3,
                "ship_from": "Москва",
                "ship_to": "Казань",
                "cargo_types": ["furniture"],
                "weight_range": "0.0-500.0 кг",
                "is_express": False
            }]
        }

        with patch('src.agents.tools.django_client.search_tariffs', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = mock_offers

            with patch('src.agents.tools.django_client.create_order', new_callable=AsyncMock) as mock_order:
                mock_order.return_value = {
                    "id": 1,
                    "order_number": f"ORD-TEST-{uuid.uuid4().hex[:6]}"
                }

                with patch('src.agents.tools.django_client.create_payment', new_callable=AsyncMock) as mock_payment:
                    mock_payment.return_value = {
                        "id": 1,
                        "status": "pending",
                        "payment_url": "https://test.com/pay/123"
                    }

                    with patch('src.agents.tools.django_client.pay_payment', new_callable=AsyncMock) as mock_pay:
                        mock_pay.return_value = {"status": "paid"}

                        print(f"\n🔑 Session ID: {session_id}")

                        # Шаг 1: Отправляем запрос
                        print("\n📝 Шаг 1: Отправка запроса...")
                        response = auth_client.post(
                            "/api/chat/process",
                            json={
                                "text": "Перевези диван из Москвы в Казань, вес 50 кг, 20.07.2026",
                                "session_id": session_id
                            }
                        )
                        print(f"📊 Статус: {response.status_code}")
                        data = response.json()
                        print(f"💬 Ответ: {data['message'][:200]}")
                        print(f"📦 Оферов: {len(data.get('offers', []))}")

                        assert response.status_code == 200
                        assert len(data["offers"]) > 0, "Нет оферов!"
                        print("✅ Шаг 1 пройден")

                        # Шаг 2: Выбираем вариант
                        print("\n📝 Шаг 2: Выбор варианта...")
                        response = auth_client.post(
                            "/api/chat/process",
                            json={"text": "1", "session_id": session_id}
                        )
                        assert response.status_code == 200
                        data = response.json()
                        print(f"💬 Ответ: {data['message'][:200]}")
                        assert "Подтвердите заказ" in data[
                            "message"], f"Ожидалось 'Подтвердите заказ', получили: {data['message']}"
                        print("✅ Шаг 2 пройден")

                        # Шаг 3: Подтверждаем
                        print("\n📝 Шаг 3: Подтверждение...")
                        response = auth_client.post(
                            "/api/chat/process",
                            json={"text": "да", "session_id": session_id}
                        )
                        assert response.status_code == 200
                        data = response.json()
                        print(f"💬 Ответ: {data['message'][:200]}")
                        assert "создан" in data["message"], f"Ожидалось 'создан', получили: {data['message']}"
                        print("✅ Шаг 3 пройден")

                        # Шаг 4: Оплачиваем
                        print("\n📝 Шаг 4: Оплата...")
                        response = auth_client.post(
                            "/api/chat/process",
                            json={"text": "оплатить", "session_id": session_id}
                        )
                        assert response.status_code == 200
                        data = response.json()
                        print(f"💬 Ответ: {data['message'][:200]}")
                        assert "оплачен" in data["message"], f"Ожидалось 'оплачен', получили: {data['message']}"
                        print("✅ Шаг 4 пройден")

                        print("\n🎉 ТЕСТ УСПЕШНО ЗАВЕРШЁН!")