import hashlib
from fastapi import Depends, HTTPException, status
from app.core.security import verify_api_key
from app.core.redis_client import redis_client

# redis limit config

REQUEST_Limit = 2
TIME_WINDOW = 60


async def rate_limit(api_key: str = Depends(verify_api_key)):
    # hash API key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    redis_key = f"rate_limit:{key_hash}"
    # Automic redis operations
    script = """
    local count = redis.call('INCR', KEYS[1])
    if count == 1 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    return count
    """
    request_count = await redis_client.eval(script, 1, redis_key, TIME_WINDOW)
    if request_count > REQUEST_Limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again after one minute.",
        )
    return request_count
