from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import concurrent_status_service, concurrent_continuation_service, content_caching_service
from app.validation import validation_schema
from app.constants import endpoint_constants
from flask import Blueprint, Response

crawler = Blueprint('crawler', __name__)



@crawler.route(endpoint_constants.CRAWLER_STATUS, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_crawler_status_get() -> Response:
    return concurrent_status_service.get_crawler_active_status()


@crawler.route(endpoint_constants.CRAWLER_STATUS_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_crawler_status_reading_post() -> Response:
    return concurrent_status_service.get_and_set_crawler_active_status()


@crawler.route(endpoint_constants.CRAWLER_STATUS_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentWritingSchema)
def handle_crawler_status_writing_post() -> Response:
    return concurrent_status_service.set_crawler_active_status()


@crawler.route(endpoint_constants.CRAWLER_CONTINUATION_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_crawler_continuation_reading_post() -> Response:
    return concurrent_continuation_service.get_and_set_crawler_continuation_status()


@crawler.route(endpoint_constants.CRAWLER_CONTINUATION_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentContinuationWritingSchema)
def handle_crawler_continuation_writing_post() -> Response:
    return concurrent_continuation_service.set_crawler_continuation_status()


@crawler.route(endpoint_constants.LAST_URL, methods=['POST'])
@validate_with_schema(validation_schema.LastUrlSchema)
def handle_last_url_post() -> Response:
    return content_caching_service.set_last_url()


@crawler.route(endpoint_constants.LAST_URL, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_last_url_get() -> Response:
    return content_caching_service.get_last_url()