import redis.asyncio as redis
from src.config import Config

JTI_EXPIRE = 3600

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True,  # important: returns str instead of bytes
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRE)

async def token_in_blocklist(jti: str) -> bool:
    value = await token_blocklist.get(jti)
    return value is not None
