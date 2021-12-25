from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import concurrent_status_service, concurrent_continuation_service, content_caching_service
from app.validation import validation_schema
from app.constants import endpoint_constants
from flask import Blueprint, Response

parser = Blueprint('parser', __name__)



@parser.route(endpoint_constants.PARSER_STATUS, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parser_status_get() -> Response:
    return concurrent_status_service.get_parser_active_status()


@parser.route(endpoint_constants.PARSER_STATUS_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_parser_status_reading_post() -> Response:
    return concurrent_status_service.get_and_set_parser_active_status()


@parser.route(endpoint_constants.PARSER_STATUS_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentWritingSchema)
def handle_parser_status_writing_post() -> Response:
    return concurrent_status_service.set_parser_active_status()


@parser.route(endpoint_constants.PARSER_CONTINUATION_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_parser_continuation_reading_post() -> Response:
    return concurrent_continuation_service.get_and_set_parser_continuation_status()


@parser.route(endpoint_constants.PARSER_CONTINUATION_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentContinuationWritingSchema)
def handle_parser_continuation_writing_post() -> Response:
    return concurrent_continuation_service.set_parser_continuation_status()


@parser.route(endpoint_constants.LAST_PARSED, methods=['POST'])
@validate_with_schema(validation_schema.LastParsedSchema)
def handle_last_parsed_post() -> Response:
    return content_caching_service.set_last_parsed()


@parser.route(endpoint_constants.LAST_PARSED, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_last_parsed_get() -> Response:
    return content_caching_service.get_last_parsed()