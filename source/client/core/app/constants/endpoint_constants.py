from app.config import env_config
# Own Endpoints
# GET Endpoints

# HTML template response
DEFAULT = "/"
HOME = "/home"
ERROR = "/error"
ACTIVITY = "/activity"
CONFIGURATION = "/configuration"
ARCHIVE = "/archive"

# JSON response
CRAWLER_STATUS = "/crawler-status"
PARSER_STATUS = "/parser-status"
MEMORY_LIMIT = "/memory-limit"

STATISTICS_PUBLIC_CHART = "/public-stats-chart"
STATISTICS_PRIVATE_CHART = "/auth-stats-chart"
STATISTICS_PUBLIC = "/public-stats"
STATISTICS_PRIVATE = "/auth-stats"

# POST Endpoints
REGISTRATION = "/registration"
AUTHENTICATION = "/authentication"
UNAUTHENTICATION = "/unauthentication"

AUTHORIZATION = "/authorization"
REFRESHMENT = "/refreshment"

CONFIRMATION = "/confirmation"
CONFIRMATION_RESENDING = "/confirmation-resending"
PASSWORD_RESETTING = "/password-resetting"
PASSWORD_FORGOTTEN = "/password-forgotten"

EMAIL_CONFIRMATION = "/email-confirmation"
EMAIL_PASSWORD_RESET = "/email-password-reset"

CRAWLER_START = "/crawler-start"
CRAWLER_STOP = "/crawler-stop"

CRAWLER_CONFIGURATION = "/crawler-configuration"
PARSER_CONFIGURATION = "/parser-configuration"
PARSER_CONFIGURATION_INSERTION = "/parser-configuration-insertion"
PARSER_CONFIGURATION_DELETION = "/parser-configuration-deletion"
CRAWLER_CONFIGURATION_OPTION = "/crawler-configuration-option"

AUTH_MS_URL = f"http://{env_config.AUTH_CONTAINER_NAME}:{env_config.AUTH_PORT}"
NOTIFICATION_MS_URL = f"http://{env_config.NOTIFICATION_CONTAINER_NAME}:{env_config.NOTIFICATION_PORT}"
CRAWLER_MS_URL = f"http://{env_config.CRAWLER_CONTAINER_NAME}:{env_config.CRAWLER_PORT}"
CONFIG_MS_URL = f"http://{env_config.CONFIG_CONTAINER_NAME}:{env_config.CONFIG_PORT}"
PARSER_MS_URL = f"http://{env_config.PARSER_CONTAINER_NAME}:{env_config.PARSER_PORT}"
STORAGE_MS_URL = f"http://{env_config.STORAGE_CONTAINER_NAME}:{env_config.STORAGE_PORT}"
STATISTICS_MS_URL = f"http://{env_config.STATISTICS_CONTAINER_NAME}:{env_config.STATISTICS_PORT}"
