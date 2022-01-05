from app.config import env_config

# Own endpoints
CRAWLER_START = "/crawler-start"
CRAWLER_STOP = "/crawler-stop"
CRAWLER_STATUS = "/crawler-status"

# Foreign endpoints
CRAWLER_CONFIGURATION = "/crawler-configuration"

MEMORY_LIMIT = "/memory-limit"
URL_STORAGE = "/url-storage"
NEXT_URL = "/next-url"

MEMORY_USAGE = "/memory-usage"
CONCURRENT_STATUS_READING = "/crawler-status-reading"
CONCURRENT_STATUS_WRITING = "/crawler-status-writing"
CONCURRENT_CONTINUATION_READING = "/crawler-continuation-reading"
CONCURRENT_CONTINUATION_WRITING = "/crawler-continuation-writing"
LAST_URL = "/last-url"

CACHE_MS_URL = f"http://{env_config.CACHE_CONTAINER_NAME}:{env_config.CACHE_PORT}"
STORAGE_MS_URL = f"http://{env_config.STORAGE_CONTAINER_NAME}:{env_config.STORAGE_PORT}"
CONFIG_MS_URL = f"http://{env_config.CONFIG_CONTAINER_NAME}:{env_config.CONFIG_PORT}"