# tests/conftest.py
import sys
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

# Добавляем src в PYTHONPATH
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def auth_client():
    """
    Создаёт тестового пользователя, получает токен и возвращает клиент с заголовками.
    Использование: def test_something(auth_client):
    """
    client = TestClient(app)

    # 1. Регистрируем пользователя (если уже существует, игнорируем ошибку)
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "89991112233"
    }
    client.post("/api/auth/register", json=register_data)

    # 2. Получаем токен
    response = client.post(
        "/api/auth/token",
        json={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    access_token = response.json().get("access")

    # 3. Создаём клиент с заголовками
    auth_client = TestClient(app)
    auth_client.headers.update({"Authorization": f"Bearer {access_token}"})

    return auth_client


@pytest.fixture(autouse=True)
def set_test_mode():
    """Включает тестовый режим для всех тестов."""
    os.environ["TEST_MODE"] = "true"
    yield
    os.environ["TEST_MODE"] = "false"