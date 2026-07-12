"""Хранение диалога"""
import os
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.checkpoint.memory import MemorySaver
import logging

logger = logging.getLogger(__name__)


async def get_redis_checkpointer():
    # Если тестовый режим — используем MemorySaver
    if os.getenv("TEST_MODE", "false").lower() == "true":
        logger.info("🧪 Тестовый режим: используем MemorySaver вместо Redis")
        return MemorySaver()

    redis_url = os.getenv("REDIS_STORAGE_URL", "redis://redis-storage:6379/0")
    logger.info(f"Подключение к Redis по URL: {redis_url}")
    try:
        checkpointer = AsyncRedisSaver(redis_url)
        await checkpointer.asetup()
        logger.info(f"✅ Redis успешно подключился по адресу {redis_url}")
        return checkpointer
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Redis: {e}")
        raise