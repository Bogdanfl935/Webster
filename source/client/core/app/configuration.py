from flask import Response, Blueprint, request
from app.constants import endpoint_constants, configuration_endpoint_handler_constants
from app.service import config_service
from app.service.authorization_service import require_access_token

configuration = Blueprint('configuration', __name__)

@configuration.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        crawler_configuration_endpoint=configuration_endpoint_handler_constants.HANDLE_CRAWLER_CONFIGURATION_PUT,
        parser_configuration_insertion_endpoint=configuration_endpoint_handler_constants.HANDLE_PARSER_CONFIGURATION_POST,
        parser_configuration_deletion_endpoint=configuration_endpoint_handler_constants.HANDLE_PARSER_CONFIGURATION_DELETE
    )

@configuration.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['POST'])
@require_access_token
def handle_crawler_configuration_put(response_object: Response, authenticated_user: str) -> str:
    return config_service.make_crawler_configuration_put(response_object, authenticated_user)

@configuration.route(endpoint_constants.PARSER_CONFIGURATION_INSERTION, methods=['POST'])
@require_access_token
def handle_parser_configuration_post(response_object: Response, authenticated_user: str) -> str:
    return config_service.make_parser_configuration_post(response_object, authenticated_user)

@configuration.route(endpoint_constants.PARSER_CONFIGURATION_DELETION, methods=['POST'])
@require_access_token
def handle_parser_configuration_delete(response_object: Response, authenticated_user: str) -> str:
    return config_service.make_parser_configuration_delete(response_object, authenticated_user)
     
