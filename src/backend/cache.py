import redis
import json
import logging
from src.backend import config

# KAN-490: Develop a cache for frequent query responses.

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=0,
                decode_responses=True
            )
            self.client.ping()
            logging.info("Successfully connected to Redis cache.")
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Could not connect to Redis: {e}. Caching will be disabled.")
            self.client = None

    def get(self, key):
        """
        Get a value from the cache.
        Logs a 'cache hit'.
        """
        if not self.client:
            return None
        
        value = self.client.get(key)
        if value:
            logging.info(f"Cache hit for key: {key}")
            return json.loads(value)
        
        logging.info(f"Cache miss for key: {key}")
        return None

    def set(self, key, value, ttl=config.CACHE_TTL_SECONDS):
        """
        Set a value in the cache with a TTL.
        """
        if not self.client:
            return
        
        try:
            self.client.set(key, json.dumps(value), ex=ttl)
            logging.info(f"Set cache for key: {key} with TTL: {ttl}s")
        except Exception as e:
            logging.error(f"Failed to set cache for key {key}: {e}")

    def invalidate(self, key):
        """
        Invalidate a specific key in the cache.
        """
        if not self.client:
            return
        
        self.client.delete(key)
        logging.info(f"Invalidated cache for key: {key}")

# Instantiate a global cache object
cache = RedisCache()
