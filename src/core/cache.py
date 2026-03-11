import logging
import pickle
import redis
from datetime import datetime
from collections import deque
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class AdvancedCache:
    """Advanced cache with Redis and Memory fallback."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_type = config.get("cache", {}).get("type", "memory")
        
        if self.cache_type == "redis":
            try:
                self.redis_client = redis.from_url(config["cache"]["redis_url"])
                self.ttl = config["cache"]["ttl"]
                self.compression = config["cache"]["compression"]
            except Exception as e:
                logger.error(f"Failed to initialize Redis: {e}. Falling back to memory.")
                self.cache_type = "memory"
                self._init_memory_cache()
        else:
            self._init_memory_cache()

    def _init_memory_cache(self):
        self.cache: Dict[str, Any] = {}
        self.access_order = deque()
        self.timestamps: Dict[str, datetime] = {}
        self.max_size = self.config.get("cache", {}).get("max_size", 1000)
        self.ttl_seconds = self.config.get("cache", {}).get("ttl", 3600)

    def get(self, key: str) -> Optional[Any]:
        if self.cache_type == "redis":
            try:
                data = self.redis_client.get(key)
                if data:
                    if self.compression:
                        import gzip
                        data = gzip.decompress(data)
                    return pickle.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None
        else:
            if key not in self.cache:
                return None
            
            if (datetime.now() - self.timestamps[key]).total_seconds() > self.ttl_seconds:
                self.remove(key)
                return None
            
            return self.cache[key]

    def put(self, key: str, value: Any):
        if self.cache_type == "redis":
            try:
                data = pickle.dumps(value)
                if self.compression:
                    import gzip
                    data = gzip.compress(data)
                self.redis_client.setex(key, self.ttl, data)
            except Exception as e:
                logger.error(f"Redis put error: {e}")
        else:
            if len(self.cache) >= self.max_size:
                lru_key = self.access_order.popleft()
                self.remove(lru_key)
            
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
            self.access_order.append(key)

    def remove(self, key: str):
        if self.cache_type == "redis":
            self.redis_client.delete(key)
        else:
            self.cache.pop(key, None)
            self.timestamps.pop(key, None)
            try:
                self.access_order.remove(key)
            except ValueError:
                pass
