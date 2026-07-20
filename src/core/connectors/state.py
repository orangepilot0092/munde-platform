import os
import redis
from datetime import datetime
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class StateManager:
    def __init__(self, connector_id: str):
        self.connector_id = connector_id
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )
        self.key = f"sahyadri:connector:state:{connector_id}"

    def get_last_sync(self):
        return self.redis_client.hget(self.key, "last_sync")

    def update_last_sync(self):
        now = datetime.utcnow().isoformat()
        self.redis_client.hset(self.key, "last_sync", now)
        self.redis_client.hincrby(self.key, "run_count", 1)

    def generate_timestamp(self):
        return datetime.utcnow().strftime("%Y%m%dT%H%M%S")
