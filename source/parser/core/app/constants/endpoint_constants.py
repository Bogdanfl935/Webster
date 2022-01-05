from app.config import env_config

# Own endpoints
PARSER_STATUS = "/parser-status"

# Foreign endpoints 
PARSED_CONTENT = "/parsed-content"
PARSED_IMAGE = "/parsed-image"
URL_STORAGE = "/url-storage"
MEMORY_LIMIT = "/memory-limit"

MEMORY_USAGE = "/memory-usage"
LAST_PARSED = "/last-parsed"

PARSER_CONFIGURATION = "/parser-configuration"

CACHE_MS_URL = f"http://{env_config.CACHE_CONTAINER_NAME}:{env_config.CACHE_PORT}"
STORAGE_MS_URL = f"http://{env_config.STORAGE_CONTAINER_NAME}:{env_config.STORAGE_PORT}"
CONFIG_MS_URL = f"http://{env_config.CONFIG_CONTAINER_NAME}:{env_config.CONFIG_PORT}"