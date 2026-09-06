from app.redis_client import redis_client
from fastapi import HTTPException,Request


async def rate_limiter(request:Request):
    client_ip = request.client.host
    key = f"rate-limit:{client_ip}"

    count = await redis_client.incr(key)

    if count == 1:
        await redis_client.expire(key,60)

    if count > 5 :
        raise HTTPException(
            status_code=429,
            detail="Too many requests."
        )
            
        