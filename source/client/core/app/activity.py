from flask import Response, Blueprint
from app.constants import endpoint_constants, activity_endpoint_handler_constants
from app.service import activity_service
from app.service.authorization_service import require_access_token

activity = Blueprint('activity', __name__)


@activity.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        crawler_status_endpoint = activity_endpoint_handler_constants.HANDLE_CRAWLER_STATUS_GET,
        parser_status_endpoint = activity_endpoint_handler_constants.HANDLE_PARSER_STATUS_GET,
        crawler_start_endpoint = activity_endpoint_handler_constants.HANDLE_CRAWLER_START_POST,
        crawler_stop_endpoint = activity_endpoint_handler_constants.HANDLE_CRAWLER_STOP_POST
    )

@activity.route(endpoint_constants.CRAWLER_STATUS, methods=['GET'])
@require_access_token
def handle_crawler_status_get(response_object: Response, authenticated_user: str) -> Response:
    return activity_service.get_crawler_status(response_object, authenticated_user)

@activity.route(endpoint_constants.PARSER_STATUS, methods=['GET'])
@require_access_token
def handle_parser_status_get(response_object: Response, authenticated_user: str) -> Response:
    return activity_service.get_parser_status(response_object, authenticated_user)


@activity.route(endpoint_constants.CRAWLER_START, methods=['POST'])
@require_access_token
def handle_crawler_start_post(response_object: Response, authenticated_user: str) -> Response:
    return activity_service.start_crawling(response_object, authenticated_user)

@activity.route(endpoint_constants.CRAWLER_STOP, methods=['POST'])
@require_access_token
def handle_crawler_stop_post(response_object: Response, authenticated_user: str) -> Response:
    return activity_service.stop_crawling(response_object, authenticated_user)