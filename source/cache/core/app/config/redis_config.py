from app.config.env_config import REDIS_CONTAINER_NAME, REDIS_PORT, REDIS_PASSWORD
import redis

redis_memory_usage = redis.Redis(host=REDIS_CONTAINER_NAME, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
redis_crawler_status = redis.Redis(host=REDIS_CONTAINER_NAME, port=REDIS_PORT, password=REDIS_PASSWORD, db=1)
redis_crawler_continuation = redis.Redis(host=REDIS_CONTAINER_NAME, port=REDIS_PORT, password=REDIS_PASSWORD, db=2)
redis_last_url = redis.Redis(host=REDIS_CONTAINER_NAME, port=REDIS_PORT, password=REDIS_PASSWORD, db=3)

redis_last_parsed = redis.Redis(host=REDIS_CONTAINER_NAME, port=REDIS_PORT, password=REDIS_PASSWORD, db=4)