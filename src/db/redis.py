from redis.asyncio import Redis
from src.config import settings

token_blocklist = Redis(host=settings.REDIS_HOST,
                         port=settings.REDIS_PORT,
                           db=0)

JTI_EXPIRY=3600

async def add_jti_to_blocklist(jti: str) :
    await token_blocklist.set(name=jti, value="",
                               ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) :
    result = await token_blocklist.get(jti)
    return result is not None