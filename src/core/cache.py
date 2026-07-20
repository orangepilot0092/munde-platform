import json
import redis
from functools import wraps
from typing import Callable, Any
from src.core.logging_config import get_logger

logger = get_logger(__name__)

# Initialize Redis client (using environment variables in production)
redis_client = redis.Redis(
    host="redis", port=6379, decode_responses=True, socket_connect_timeout=2
)


def cache_response(ttl: int = 300):
    """Decorator to cache FastAPI response in Redis."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate a simple cache key based on function name and args
            key = f"sahyadri:{func.__name__}:{str(kwargs)}"

            try:
                # Try to get from cache
                cached_data = redis_client.get(key)
                if cached_data:
                    logger.info(f"Cache hit for {key}")
                    return json.loads(cached_data)

                # Call the actual function
                result = await func(*args, **kwargs)

                # Store in cache
                if result:
                    redis_client.setex(key, ttl, json.dumps(result))
                    logger.info(f"Cache set for {key} with TTL {ttl}s")

                return result
            except redis.exceptions.ConnectionError as e:
                logger.warning(f"Redis connection failed, bypassing cache: {e}")
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Cache error for {key}: {e}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator
