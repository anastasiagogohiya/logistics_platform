#!/usr/bin/env python3
import secrets
from pathlib import Path


def generate_secret(length=32):
    return secrets.token_hex(length)


def generate_password(length=16):
    return secrets.token_hex(length)


def create_env():
    env_file = Path('.env')

    # Проверяем, существует ли .env
    if env_file.exists():
        print("⚠️  .env уже существует!")
        response = input("Перезаписать? (y/N): ")
        if response.lower() != 'y':
            print("❌ Отменено.")
            return

    print("🔑 Генерация ключей...")

    # Генерируем ключи
    SECRET_KEY = generate_secret()
    DJANGO_SECRET_KEY = generate_secret()
    POSTGRES_PASSWORD = generate_password()
    FASTAPI_SECRET_KEY = generate_secret()
    SIGNING_KEY = generate_secret()  # Для HS256 просто hex-строка

    # Создаем .env
    env_content = f'''# ==========================================
# 🐍 DJANGO SETTINGS
# ==========================================
SECRET_KEY={SECRET_KEY}
SIGNING_KEY={SIGNING_KEY}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_API_URL=http://django:8001
DJANGO_TIMEOUT=5

# ==========================================
# 🐘 POSTGRESQL
# ==========================================
POSTGRES_DB=logistics_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD={POSTGRES_PASSWORD}
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ==========================================
# 🚀 FASTAPI SETTINGS
# ==========================================
FASTAPI_SECRET_KEY={FASTAPI_SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://redis-storage:6379/0

# ==========================================
# 📨 KAFKA
# ==========================================
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# ==========================================
# 🌍 ОБЩИЕ НАСТРОЙКИ
# ==========================================
ENVIRONMENT=development

# ==========================================
# 🔧 ДЛЯ ПРОДАКШЕНА (закомментировано)
# ==========================================
# DEBUG=False
# ENVIRONMENT=production
# ALLOWED_HOSTS=your-domain.com,www.your-domain.com
'''

    with open('.env', 'w') as f:
        f.write(env_content)

    print("✅ .env создан!")
    print("")
    print("📋 Сгенерированные ключи:")
    print(f"  SECRET_KEY: {SECRET_KEY}")
    print(f"  SIGNING_KEY: {SIGNING_KEY}")
    print(f"  FASTAPI_SECRET_KEY: {FASTAPI_SECRET_KEY}")
    print(f"  POSTGRES_PASSWORD: {POSTGRES_PASSWORD}")
    print("  ALGORITHM: HS256")
    print("")
    print("🚀 Теперь запустите: just up")


if __name__ == '__main__':
    create_env()