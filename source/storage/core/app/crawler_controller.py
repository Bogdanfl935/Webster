from flask import Blueprint, Response
from app.constants import  endpoint_constants
from app.services import url_storage_service
from app.services.validation_service import validate_with_schema
from app.validation import validation_schema

crawler = Blueprint('crawler', __name__)


@crawler.route(endpoint_constants.URL_STORAGE, methods=['POST'])
@validate_with_schema(validation_schema.UrlInsertionSchema)
def handle_url_storage_post() -> Response:
    return url_storage_service.add_bulk_urls()


@crawler.route(endpoint_constants.URL_STORAGE, methods=['PUT'])
@validate_with_schema(validation_schema.UrlUpdateSchema)
def handle_url_storage_put() -> Response:
    return url_storage_service.update_bulk_pending_url_states()


@crawler.route(endpoint_constants.NEXT_URL, methods=['POST'])
@validate_with_schema(validation_schema.UrlRetrievalSchema)
def handle_next_url_post() -> Response:
    return url_storage_service.fetch_next_urls()