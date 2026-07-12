import redis.asyncio as redis
import os
import json
from typing import Any, Dict

REDIS_STORAGE_URL = os.getenv("REDIS_STORAGE_URL", "redis://redis-storage:6380/0")
TTL = 3600  # время жизни сессии в секундах (1 час)

_redis_client = None

async def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_STORAGE_URL, decode_responses=True)
    return _redis_client

async def get_session_data(session_id: str) -> Dict[str, Any]:
    r = await get_redis()
    key = f"chat:session:{session_id}"
    data = await r.get(key)
    if data:
        return json.loads(data)
    return {}

async def set_session_data(session_id: str, data: Dict[str, Any]) -> None:
    r = await get_redis()
    key = f"chat:session:{session_id}"
    await r.setex(key, TTL, json.dumps(data, default=str))

async def delete_session(session_id: str) -> None:
    r = await get_redis()
    key = f"chat:session:{session_id}"
    await r.delete(key)