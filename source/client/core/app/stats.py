from flask import Response, Blueprint
from app.constants import endpoint_constants, stats_endpoint_handler_constants
from app.service import statistics_service
from app.service.authorization_service import require_access_token

stats = Blueprint('stats', __name__)

@stats.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        public_statistics_chart_endpoint=stats_endpoint_handler_constants.HANDLE_STATISTICS_PUBLIC_CHART_GET,
        auth_statistics_chart_endpoint=stats_endpoint_handler_constants.HANDLE_STATISTICS_PRIVATE_CHART_GET,
        public_statistics_endpoint=stats_endpoint_handler_constants.HANDLE_STATISTICS_PUBLIC_GET,
        auth_statistics_endpoint=stats_endpoint_handler_constants.HANDLE_STATISTICS_PRIVATE_GET
    )

@stats.route(endpoint_constants.STATISTICS_PUBLIC_CHART, methods=['GET'])
def handle_statistics_public_chart_get() -> str:
    return statistics_service.make_statistics_public_chart_get()

@stats.route(endpoint_constants.STATISTICS_PUBLIC, methods=['GET'])
def handle_statistics_public_get() -> str:
    return statistics_service.make_statistics_public_get()

@stats.route(endpoint_constants.STATISTICS_PRIVATE_CHART, methods=['GET'])
@require_access_token
def handle_statistics_private_chart_get(response_object: Response, authenticated_user: str) -> str:
    return statistics_service.make_statistics_private_chart_get(response_object, authenticated_user)

@stats.route(endpoint_constants.STATISTICS_PRIVATE, methods=['GET'])
@require_access_token
def handle_statistics_private_get(response_object: Response, authenticated_user: str) -> str:
    return statistics_service.make_statistics_private_get(response_object, authenticated_user)
     
