from flask import Blueprint, Response
from app.constants import endpoint_constants, archive_endpoint_handler_constants
from app.service import archive_service, storage_service
from app.service.authorization_service import require_access_token
from urllib.parse import urlparse

archive = Blueprint('archive', __name__)

@archive.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        export_content_endpoint=archive_endpoint_handler_constants.HANDLE_EXPORT_CONTENT_GET,
        parsed_content_endpoint=archive_endpoint_handler_constants.HANDLE_PARSED_CONTENT_DELETE,
        parsed_image_endpoint=archive_endpoint_handler_constants.HANDLE_PARSED_IMAGE_DELETE,
        get_hostname = lambda url: urlparse(url).netloc
    )

@archive.route(endpoint_constants.EXPORT_CONTENT, methods=['GET'])
@require_access_token
def handle_export_content_get(response_object: Response, authenticated_user: str) -> str:
    return archive_service.make_export_content_get(response_object, authenticated_user)

@archive.route(endpoint_constants.PARSED_CONTENT, methods=['DELETE'])
@require_access_token
def handle_parsed_content_delete(response_object: Response, authenticated_user: str) -> str:
    return archive_service.make_parsed_content_delete(response_object, authenticated_user)

@archive.route(endpoint_constants.PARSED_IMAGE, methods=['DELETE'])
@require_access_token
def handle_parsed_image_delete(response_object: Response, authenticated_user: str) -> str:
    return archive_service.make_parsed_image_delete(response_object, authenticated_user)