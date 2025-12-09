import aioredis
from app.core.config import settings
import json
from enum import Enum

redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)

def json_serializer(obj):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")

async def get_cached(key: str):
    return await redis.get(key)

async def set_cache(key: str, value, expire: int = 60):
    if value is None:
        await redis.delete(key)
    else:
        await redis.set(key, json.dumps(value, default=json_serializer), ex=expire)
