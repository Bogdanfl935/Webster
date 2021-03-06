from app.config import env_config
MEMORY_USAGE = "/memory-usage"


CRAWLER_STATUS = "/crawler-status"
CRAWLER_STATUS_READING = "/crawler-status-reading"
CRAWLER_STATUS_WRITING = "/crawler-status-writing"
CRAWLER_CONTINUATION_READING = "/crawler-continuation-reading"
CRAWLER_CONTINUATION_WRITING = "/crawler-continuation-writing"
LAST_URL = "/last-url"

LAST_PARSED = "/last-parsed"

STORAGE_MS_URL = f"http://{env_config.STORAGE_CONTAINER_NAME}:{env_config.STORAGE_PORT}"
