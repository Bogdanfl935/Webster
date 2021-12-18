import json

from app.config.redis_config import redis_memory_usage


def modify_memory_usage(username, memory_usage):
    redis_memory_usage.incr(username, memory_usage)


def get_memory_usage(username):
    return json.dumps({"username": username, "memoryUsage": str(redis_memory_usage.get(username).decode('utf-8'))})
